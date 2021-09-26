#required imports
from qiskit import *
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from math import pi

#helper functions
def convert_decimal_to_binary(arr,m):
    number_of_bits_string = "0" + str(m) + "b"
    for i in range(len(arr)):
        arr[i] = format(arr[i], number_of_bits_string)
    return arr

#main function 
def quantum_circuit(binary_arr,n,m):
    assert int(pow(2,n)) == len(binary_arr) , "Number of elemenrts in the array not equal to 2^n"
    assert m >= 2 , '"m" must be greater than or equal to 2'
    address = QuantumRegister(n,'address')
    data = QuantumRegister(m,'data')
    temp = QuantumRegister(7,'oracle')
    flag = QuantumRegister(1,'flag')
    c = ClassicalRegister(n)
    qc = QuantumCircuit(address,data,temp,flag,c)
    
    #Get set of odd and even data registers for the oracle
    even_register = []
    odd_register = []
    for k in range(m):
        if k%2 == 0:
            even_register.append(data[k])
        else:
            odd_register.append(data[k])
    
    qc.ry(-(pi/2),flag)
    qc.h(address)
    #QRAM 
    for i in range(len(binary_arr)):
        itr = convert_decimal_to_binary([i],n)
        for j in range(len(itr[0])):
            if itr[0][j] == '0':
                qc.x(address[j])
        for j in range(len(binary_arr[i])):
            if binary_arr[i][j] == '1':
                qc.mct(address,data[j])
        for j in range(len(itr[0])):
            if itr[0][j] == '0':
                qc.x(address[j])
        qc.barrier()

    #Oracle
    qc.barrier()

    qc.mct(odd_register, temp[0])
    qc.x(temp[1])
    qc.mct(even_register, temp[1])
    qc.ccx(temp[0],temp[1],temp[2])
    
    qc.barrier()
    
    qc.x(temp[3])
    qc.mct(odd_register, temp[3])
    qc.mct(even_register, temp[4])
    qc.ccx(temp[3],temp[4],temp[5])
    
    qc.barrier()
    qc.ccx(temp[2],temp[5],temp[6])

    qc.cx(temp[6],flag)

    qc.ccx(temp[2],temp[5],temp[6])
    qc.barrier()
    
    qc.x(temp[3])
    qc.mct(odd_register, temp[3])
    qc.mct(even_register, temp[4])
    qc.ccx(temp[3],temp[4],temp[5])
    
    qc.barrier()
    
    qc.mct(odd_register, temp[0])
    qc.x(temp[1])
    qc.mct(even_register, temp[1])
    qc.ccx(temp[0],temp[1],temp[2])
    
    qc.barrier()
    #QRAM 
    for i in range(len(binary_arr)):
        itr = convert_decimal_to_binary([i],n)
        for j in range(len(itr[0])):
            if itr[0][j] == '0':
                qc.x(address[j])
        for j in range(len(binary_arr[i])):
            if binary_arr[i][j] == '1':
                qc.mct(address,data[j])
        for j in range(len(itr[0])):
            if itr[0][j] == '0':
                qc.x(address[j])
        qc.barrier()

    #Diffuser
    nqubits = n
    for qubit in range(nqubits):
        qc.h(qubit)
    for qubit in range(nqubits):
        qc.x(qubit)
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)
    qc.h(nqubits-1)
    for qubit in range(nqubits):
        qc.x(qubit)
    for qubit in range(nqubits):
        qc.h(qubit)

    qc.barrier()
    return qc