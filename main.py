import datetime

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, BigInteger, SmallInteger, DECIMAL, ForeignKey, Date, select
from sqlalchemy.orm import sessionmaker
from decimal import *

DATABASE_URL = "mysql+pymysql://root@localhost/banksystem"
engine = create_engine(DATABASE_URL)

Base = sqlalchemy.orm.declarative_base()

#Declaracion de tablas
class Bank(Base):
    __tablename__ = "BANK"

    id_bank = Column(Integer, primary_key=True, autoincrement=True)
    name_bank = Column(String(60), nullable=False)
    phone_bank = Column(String(20), nullable=True)

class Account(Base):
    __tablename__ = "ACCOUNT"

    id_account = Column(Integer, primary_key=True, autoincrement=True)
    id_bank = Column(Integer, ForeignKey("BANK.id_bank"), nullable=False)
    id_nationality = Column(Integer, ForeignKey("NATIONALITY.id_nationality"), nullable=False)
    number_account = Column(Integer, nullable=True)
    ci_account = Column(Integer, nullable=True)
    name_account = Column(String(50), nullable=True)
    lastname_account = Column(String(50), nullable=True)
    phone_account = Column(BigInteger, nullable=True)
    address_account = Column(String(100), nullable=True)
    balance_account = Column(DECIMAL(13,2), nullable=True)
    faults_account = Column(SmallInteger, nullable=True)

class Cheque(Base):
    __tablename__ = "CHEQUE"

    id_cheque = Column(Integer, primary_key=True, autoincrement=True)
    idemitter_account = Column(Integer, ForeignKey("ACCOUNT.id_account"), nullable=False)
    idreceptor_account = Column(Integer, ForeignKey("ACCOUNT.id_account") ,nullable=True)
    id_chequestate = Column(Integer, ForeignKey("CHEQUESTATE.id_chequestate"), nullable=False)
    payment_cheque = Column(DECIMAL(13,2), nullable=True)
    pushDate_cheque = Column(Date, nullable=True)
    endDate_cheque = Column(Date, nullable=True)
    address_cheque = Column(String(100), nullable=True)
    isdeferred_cheque = Column(SmallInteger, nullable=True)  # Se usa SmallInteger para simular booleanos

class ChequeState(Base):
    __tablename__ = "CHEQUESTATE"

    id_chequestate = Column(Integer, primary_key=True, autoincrement=True)
    state_cheque = Column(String(20), nullable=True)  # Se usa String en lugar de char(20)

class Nationality(Base):
    __tablename__ = "NATIONALITY"

    id_nationality = Column(Integer, primary_key=True, autoincrement=True)
    country_nationality = Column(String(50), nullable=True)  # Se usa String en lugar de char(50)


class Transaction(Base):
    __tablename__ = "TRANSACTION"

    id_transaction = Column(Integer, primary_key=True, autoincrement=True)
    id_bank = Column(Integer, ForeignKey("BANK.id_bank"), nullable=False)
    id_emitter_account = Column(Integer, ForeignKey("ACCOUNT.id_account"), nullable=False)
    id_receptor_account = Column(Integer, ForeignKey("ACCOUNT.id_account"), nullable=True)#puede o no tener portador
    amount_transaction = Column(DECIMAL(13,2), nullable=True)
    date_transaction = Column(Date, nullable=True)

class AccountFormated:
    def __init__(self, account:type[Account]):
        self.id_account = account.id_account
        self.bank = session.get(Bank, {"id_bank":account.id_bank})
        self.nationality = session.get(Nationality, {"id_nationality": account.id_nationality})
        self.number_account = account.number_account
        self.ci_account = account.ci_account
        self.name_account = account.name_account
        self.lastname_account = account.lastname_account
        self.phone_account = account.phone_account
        self.address_account = account.address_account
        self.balance_account = account.balance_account
        self.faults_account = account.faults_account


class ChequeFormated:
    def __init__(self, cheque:type[Cheque]):
        self.id_cheque = cheque.id_cheque
        self.emitter_account = session.get(Account, {"id_account":cheque.idemitter_account})
        self.receptor_account = session.get(Account, {"id_account":cheque.idreceptor_account})
        self.cheque_state = session.get(ChequeState, {"id_chequestate":cheque.id_chequestate}).state_cheque
        self.payment_cheque = cheque.payment_cheque
        self.pushDate_cheque = cheque.pushDate_cheque
        self.endDate_cheque = cheque.endDate_cheque
        self.address_cheque = cheque.address_cheque
        self.is_deferred_cheque = cheque.isdeferred_cheque


class TransactionFormated:
    def __init__(self, transaction:type[Transaction]):
        self.id_transaction = transaction.id_transaction
        self.bank = session.get(Bank, {"id_bank":transaction.id_bank})
        self.emitter_account = session.get(Account, {"id_account":transaction.id_emitter_account})
        self.receptor_account = session.get(Account, {"id_account":transaction.id_receptor_account})
        self.amount_transaction = transaction.amount_transaction
        self.date_transaction = transaction.date_transaction

#Agregar Banco
def add_bank(bank_name, bank_phone):
    new_bank = Bank(name_bank = bank_name, phone_bank =  bank_phone)
    session.add(new_bank)
    session.commit()

#Agregar Cuenta
def add_account(bank_id, nationality_id, account_number, ci, name, lastname, phone, address):
    new_account = Account(
        id_bank = bank_id, id_nationality = nationality_id, number_account = account_number, ci_account = ci,name_account = name,
        lastname_account = lastname,phone_account = phone, address_account = address, balance_account = Decimal("0.00"),faults_account = 0)
    session.add(new_account)
    session.commit()

#Crear Cheque
def add_cheque(id_emitter_account, id_receptor_account, id_cheque_state, payment, push_date, end_date, address, is_deferred):
    new_cheque = Cheque(
        idemitter_account = id_emitter_account,
        idreceptor_account = id_receptor_account,
        id_chequestate = id_cheque_state,
        payment_cheque = payment,
        pushDate_cheque = push_date,
        endDate_cheque = end_date,
        address_cheque = address,
        isdeferred_cheque = is_deferred
    )
    session.add(new_cheque)
    session.commit()

def get_bank(id_):
    bank = session.get(Bank, {"id_bank":id_})
    return bank

def get_nationalities():
    stmt = select(Nationality.c.country_nationality)
    nat_list = session.execute(stmt)

    return nat_list

def get_nationality_by_name(nat_name:str):
    nat = session.get(Nationality, {"country_nationality":nat_name})
    return  nat

def get_nationality_by_id(nat_id:int):
    nat = session.get(Nationality, {"id_nationality": nat_id})
    return nat

def get_cheque_state_by_name(state_name:str):
    state = session.get(ChequeState, {"state_cheque": state_name})
    return  state

def get_cheque_state_by_id(state_id:int):
    state = session.get(ChequeState, {"id_chequestate": state_id})
    return  state

#Tomar Objeto de una cuenta
def get_account_raw(id_):
    acc = session.get(Account, {"id_account": id_})
    return acc

#Obtener Objeto personalizado, reemplaza fk's por el registro al que apunta la id
def get_account_(id_):
    acc = get_account_raw(id_)
    if acc is not None:
        acc_formated = AccountFormated(acc)
        return acc_formated
    else: return None

def get_cheque_raw(id_):
    cheque = session.get(Cheque, {"id_cheque": id_})
    return cheque

#Obtener Objeto personalizado, reemplaza fk's por el registro al que apunta la id
def get_cheque_(id_):
    cheque = get_cheque_raw(id_)
    if cheque is not None:
        cheque_formated = ChequeFormated(cheque)
        return cheque_formated
    else:
        return None


def get_transaction_raw(id_):
    transaction = session.get(Transaction, {"id_transaction":id_})
    return transaction

def get_transaction_(id_):
    transaction = get_transaction_raw(id_)
    if transaction is not None:
        t = TransactionFormated(transaction)
        return t
    else: return None


#Global session reference
if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()

    cheque = get_cheque_(1)
    print(f"""
        Emisor: {cheque.emitter_account.name_account} {cheque.emitter_account.lastname_account}
        Receptor: {cheque.receptor_account.name_account} {cheque.receptor_account.lastname_account}
        Monto: {cheque.payment_cheque}
        Fecha de emision: {cheque.pushDate_cheque}
        Vence el: {cheque.endDate_cheque}
        Banco a pagar: {get_bank(cheque.emitter_account.id_bank).name_bank} 
    """)