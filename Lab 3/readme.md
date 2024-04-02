code written by Varun Deliwala (vd2298)

The lab 3 here formulates an MDP
To run the program, simply run the below mentionedl command 
```
    python3 mdp.py -tol toleranceValue -df discountValue -iter maxIterValue -min input.txt
```

The default values are set to 
df = 1.0
min  = False
tol = 0.001
maxIter = 100

Note: if all the nodes are chance nodes, the code prints only those nodes where the node only have one transition option and no other nodes, ofcourse believing that no policy exists in such cases. 
But in all the cases, the code prints the values. 
