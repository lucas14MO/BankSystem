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
    idEmitter_account = Column(Integer, ForeignKey("ACCOUNT.id_account"), nullable=False)
    idReceptor_account = Column(Integer, ForeignKey("ACCOUNT.id_account") ,nullable=True)#puede o no tener portador
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
    idEmitter_account = Column(Integer, ForeignKey("ACCOUNT.id_account"), nullable=False)
    idReceptor_account = Column(Integer, ForeignKey("ACCOUNT.id_account"), nullable=False)
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
        self.emitter_account = session.get(Account, {"id_account":cheque.idEmitter_account})
        self.receptor_account = session.get(Account, {"id_account":cheque.idReceptor_account})
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
        self.emitter_account = session.get(Account, {"id_account":transaction.idEmitter_account})
        self.receptor_account = session.get(Account, {"id_account":transaction.idReceptor_account})
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
        idEmitter_account = id_emitter_account,
        idReceptor_account = id_receptor_account,
        id_chequestate = id_cheque_state,
        payment_cheque = payment,
        pushDate_cheque = push_date,
        endDate_cheque = end_date,
        address_cheque = address,
        isdeferred_cheque = is_deferred
    )
    session.add(new_cheque)
    session.commit()

#Crear transaccion
def add_transaction(id_bank, id_emitter_acc, id_receptor_acc, amount_, date_):
    new_transaction = Transaction(
        id_bank = id_bank,
        idEmitter_account = id_emitter_acc,
        idReceptor_account = id_receptor_acc,
        amount_transaction = amount_,
        date_transaction = date_
    )
    session.add(new_transaction)
    session.commit()

def update_account(id_account_to_edit, bank_id, nationality_id, account_number, ci, name, lastname, phone, address, faults):
    acc_to_edit = get_account_raw(id_account_to_edit)
    if acc_to_edit is not None:
        acc_to_edit.id_bank = bank_id
        acc_to_edit.id_nationality = nationality_id
        acc_to_edit.number_account = account_number
        acc_to_edit.ci_account = ci
        acc_to_edit.name_account = name
        acc_to_edit.lastname_account = lastname
        acc_to_edit.phone_account = phone
        acc_to_edit.address_account = address
        acc_to_edit.faults_account = faults
        session.commit()


def set_account_balance(account_id, balance:Decimal):
    acc = session.get(Account, {"id_account": account_id})
    if acc is not None:
        acc.balance_account = balance
        session.commit()
        return 1
    else: return -1 #Indica si el setteo no se realizo


def modify_account_balance(account_id, balance: Decimal):
    acc = session.get(Account, {"id_account": account_id})
    if acc is not None:
        acc.balance_account += balance
        session.commit()
        return  1
    else: return -1 #Indica si el setteo no se realizo


def update_bank(id_bank_to_edit, bank_name, bank_phone):
    bank_to_edit = session.get(Bank, {"id_bank": id_bank_to_edit})
    if bank_to_edit is not None:
        bank_to_edit.name_bank = bank_name
        bank_to_edit.phone_bank = bank_phone
        session.commit()


def get_bank(id_):
    bank = session.get(Bank, {"id_bank":id_})
    return bank

def get_bank_by_name(name: str):
    bank = session.query(Bank).filter(Bank.name_bank == name)
    if bank.count() != 0:
        return bank.one()
    else: return None

def get_nationalities():
    stmt = select(Nationality.c.country_nationality)
    nat_list = session.execute(stmt)

    return nat_list

def get_nationality_by_name(nat_name:str):
    nat = session.query(Nationality).filter(Nationality.country_nationality == nat_name)
    if nat.count() != 0:
        return nat.one()
    else:
        return None

def get_nationality_by_id(nat_id:int):
    nat = session.get(Nationality, {"id_nationality": nat_id})
    return nat

def get_cheque_state_by_name(state_name:str):
    state = session.query(ChequeState).filter(ChequeState.state_cheque == state_name)
    if state.count() != 0:
        return state.one()
    else:
        return None

def get_cheque_state_by_id(state_id:int):
    state = session.get(ChequeState, {"id_chequestate": state_id})
    return  state

#Tomar Objeto de una cuenta
def get_account_raw(id_):
    acc = session.get(Account, {"id_account": id_})
    return acc


def get_account_from_bank(id_bank):
    accounts = session.query(Account).filter(Account.id_bank == id_bank)
    if accounts.count() != 0:
        return accounts.all()
    else: return None

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

def delete_bank(id_bank_to_delete):
    bank_to_delete = session.get(Bank, {"id_bank": id_bank_to_delete})
    if bank_to_delete is not None:
        session.delete(bank_to_delete)
        session.commit()

def delete_account(id_account_to_delete):
    account_to_delete = session.get(Account, {"id_account": id_account_to_delete})
    if account_to_delete is not None:
        session.delete(account_to_delete)
        session.commit()


session = None
#Global session reference
if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()

    m = get_bank_by_name("Ueno Bank S.A.E.C.A.")
    print(m)