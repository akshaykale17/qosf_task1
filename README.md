# Quantum Alternate Bits (QAB)
The Quantum Alternate Bits (QAB) module is designed such that it takes 3 parameters   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;n = Number of address bits  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;m = number of bits for each value  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;arr = A array with 2^n Values  
And returns a quantum circuit when measured gives superposition of states with a high probability of states that have alternating bits.  

```
arr = [1,2,5,7],n =2 ,m=3  
Output =>
{'11': 121, '01': 386, '00': 131, '10': 362}
```
States ['01', '10'] are in superposition with high probability i.e The states with alternating bits

# Module Explanation
There are 2 functions to achieve the said superposition.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1)convert_decimal_to_binary(arr,m) = function takes 2 arguments   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;arr =  the array with int values and m number of bits  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;And returns array of binary numbers  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2)quantum_circuit(binary_arr,n,m) function takes 3 arguments  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;binary_arr i.e output of convert_decimal_to_binary  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;n =  number of address bits  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;m = number of bits for each value  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;And returns a quantum circuit that gives superposition of target states.  
# Usage
## Import the Module
```python
import quantum_alternate_bits as qab
```
## Use the module functions to get the Quantum circuit.
```python
binary_arr = qab.convert_decimal_to_binary(arr,m) #converts integer array to binary array
qc = qab.quantum_circuit(binary_arr,n,m) #returns the required circuit
```
# Implementation details
QAB modules use QRAM and Grover’s algorithm to achieve this result 
## QRAM
Just like in classical computers RAM(Random access memory) is used to store important data so that the calculations can be done quickly, Qram is used in Quantum computing to get all inputs in superposition which gives the advantage to do all operations simultaneously.   
In the QAB module, we use QRAM to store all the input bits in a superposition so that we can amplify the amplitudes of the states with alternating bits.


## Grover's algorithm
Once we have a superposition of all the input states using QRAM next step is Grover’s algorithm. 
Grover’s algorithms (also called database search algorithm) amplifies the amplitude of the target states i.e states with alternating bits using an oracle. Oracle is an important part of the Grover's algorithms as it contains logic to amplify the states.

### Oracle 
In QAB module the oracle has 3 sections as mentioned below   
Section 1 targets state that has odd numbered bits as "1" and even numbered as "0". For Ex for 3 bit string it will target "010".  
Section 2 targets state that has odd numbered bits as "0" and even numbered as "1". For Ex for 3 bit string it will target "101".   
And In section 3 There is a logical AND (i.e A CCX gate) Between those 2 states so that alternating bit string are amplified. 
```python
qc.barrier() #Section 1 (odd numbered register as "1" and even "0")

qc.mct(odd_register, temp[0])
qc.x(temp[1])
qc.mct(even_register, temp[1])
qc.ccx(temp[0],temp[1],temp[2])
    
qc.barrier() #Section 2 (even numbered register as "1" and odd "0")
    
qc.x(temp[3])
qc.mct(odd_register, temp[3])
qc.mct(even_register, temp[4])
qc.ccx(temp[3],temp[4],temp[5])
    
qc.barrier() #Section 3 (Logical AND operation)
qc.ccx(temp[2],temp[5],temp[6])

qc.cx(temp[6],flag) #Flag to invert the sign of the states

#Dagger of the circuit.(i.e basically reverse of the 3 sections)
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
```
# Examples 
Check [this](https://github.com/akshaykale17/qosf_task1/blob/main/example.ipynb) JupyterNotebook to see examples.

# References
[1] Grover, Lov K.. “A fast quantum mechanical algorithm for database search.” STOC '96 (1996).  
[2] Giovannetti, Vittorio et al. "Quantum Random Access Memory". Physical Review Letters 100. 16(2008).
