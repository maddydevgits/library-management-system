from flask import Flask,render_template,redirect,request,session
from ca import *
import json
from web3 import Web3, HTTPProvider

def connect_Blockchain_register(acc):
    blockchain_address="http://127.0.0.1:7545"
    web3=Web3(HTTPProvider(blockchain_address))
    if(acc==0):
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/register.json'
    contract_address=registerContractAddress
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']

    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    print('connected with blockchain')
    return (contract,web3)

def connect_Blockchain_lms(acc):
    blockchain_address="http://127.0.0.1:7545"
    web3=Web3(HTTPProvider(blockchain_address))
    if(acc==0):
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/lms.json'
    contract_address=lmsContractAddress
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']

    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    print('connected with blockchain')
    return (contract,web3)

app=Flask(__name__)
app.secret_key='makeskilled'

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/register')
def registerPage():
    return render_template('register.html')

@app.route('/registerUser',methods=['POST','GET'])
def registerUser():
    name=request.form['name']
    walletaddr=request.form['walletaddr']
    rollno=int(request.form['rollno'])
    password=int(request.form['password'])
    print(name,walletaddr,rollno,password)
    contract,web3=connect_Blockchain_register(0)
    tx_hash=contract.functions.registerStudent(walletaddr,name,rollno,password).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('login.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/loginUser',methods=['GET','POST'])
def loginUser():
    walletaddr=request.form['walletaddr']
    password=int(request.form['password'])
    print(walletaddr,password)
    contract,web3=connect_Blockchain_register(0)
    status=contract.functions.loginStudent(walletaddr,password).call()
    print(status)
    if status==True:
        session['walletaddr']=walletaddr
        return redirect('/dashboard')
    else:
        return redirect('/login')

@app.route('/dashboard')
def dashboardPage():
    contract,web3=connect_Blockchain_register(0)
    rollNos,passwords,studentWallets,studentNames=contract.functions.viewStudents().call()
    contract,web3=connect_Blockchain_lms(0)
    book_names,book_ids,book_counts,book_a=contract.functions.viewBooks().call()

    data=[]
    for i in range(len(book_names)):
        dummy=[]
        dummy.append(book_names[i])
        dummy.append(book_ids[i])
        if(book_a[i]>0):
            dummy.append('Available')
        else:
            dummy.append('Not Available')
        data.append(dummy)
    l=len(data)
    return render_template('dashboard.html',dashboard_data=data,len=l)

@app.route('/logout')
def logout():
    session['walletaddr']=''
    return render_template('index.html')

@app.route('/admin')
def adminPage():
    return render_template('admin.html')

@app.route('/addBookForm',methods=['GET','POST'])
def addBookForm():
    bookid=int(request.form['bookid'])
    bookname=request.form['bookname']
    bookcount=int(request.form['bookcount'])
    print(bookid,bookname,bookcount)
    contract,web3=connect_Blockchain_lms(0)
    tx_hash=contract.functions.addBook(bookname,bookid,bookcount).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/aviewBooks')

@app.route('/aviewBooks')
def aviewBooks():
    contract,web3=connect_Blockchain_lms(0)
    book_names,book_ids,book_counts,book_a=contract.functions.viewBooks().call()
    data=[]
    for i in range(len(book_names)):
        dummy=[]
        dummy.append(book_names[i])
        dummy.append(book_ids[i])
        dummy.append(book_counts[i])
        dummy.append(book_a[i])
        data.append(dummy)
    l=len(data)
    return render_template('aviewBooks.html',dashboard_data=data,len=l)

@app.route('/book/<id>')
def bookRequest(id):
    print(id)
    id=int(id)
    walletaddr=session['walletaddr']
    contract,web3=connect_Blockchain_register(0)
    rollNos,passwords,studentWallets,studentNames=contract.functions.viewStudents().call()
    rollNoIndex=studentWallets.index(walletaddr)
    rollNo=rollNos[rollNoIndex]
    contract,web3=connect_Blockchain_lms(0)
    tx_hash=contract.functions.allocateBook(rollNo,id).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/viewBooks')

@app.route('/viewBooks')
def viewBooksPage():
    data=[]
    walletaddr=session['walletaddr']
    contract,web3=connect_Blockchain_register(0)
    rollNos,passwords,studentWallets,studentNames=contract.functions.viewStudents().call()
    rollNoIndex=studentWallets.index(walletaddr)
    rollNo=rollNos[rollNoIndex]
    contract,web3=connect_Blockchain_lms(0)
    _brollNo,_bbookId,_bstatus=contract.functions.listBooks().call()
    book_names,book_ids,book_counts,book_a=contract.functions.viewBooks().call()
    for i in range(len(_brollNo)):
        dummy=[]
        if _brollNo[i]==rollNo and _bstatus[i]==True:
            dummy.append(_bbookId[i])
            bookIndex=book_ids.index(_bbookId[i])
            dummy.append(book_names[bookIndex])
            data.append(dummy)
    l=len(data)
    return render_template('viewBooks.html',dashboard_data=data,len=l)

@app.route('/return/<id>')
def returnBookRequest(id):
    print(id)
    id=int(id)
    walletaddr=session['walletaddr']
    contract,web3=connect_Blockchain_register(0)
    rollNos,passwords,studentWallets,studentNames=contract.functions.viewStudents().call()
    rollNoIndex=studentWallets.index(walletaddr)
    rollNo=rollNos[rollNoIndex]
    contract,web3=connect_Blockchain_lms(0)
    tx_hash=contract.functions.returnBook(rollNo,id).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/viewBooks')

@app.route('/aviewStudents')
def aviewStudents():
    contract,web3=connect_Blockchain_lms(0)
    _brollNo,_bbookId,_bstatus=contract.functions.listBooks().call()
    data=[]
    for i in range(len(_brollNo)):
        if _bstatus[i]==True:
            dummy=[]
            dummy.append(_brollNo[i])
            dummy.append(_bbookId[i])
            data.append(dummy)
    l=len(data)
    return render_template('aviewStudents.html',dashboard_data=data,len=l)
    
if __name__=="__main__":
    app.run(debug=True)