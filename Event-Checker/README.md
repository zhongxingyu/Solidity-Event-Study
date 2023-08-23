# Problematic Event Logging Parameter Checker for Gas Saving
To show the feasibility of automatic event logging assistance from our findings, we design a simple problematic event logging parameter checker which helps identify gas saving opportunities. 

The checker is motivated by the non-neglectable number of parameter changes that replace Storage type variable with Memory type variable. The reason is after compiling the event use to EVM bytecode, an extra Sload EVM operation would be needed to access the variable if it is storage type, and the Sload operation costs 800 gas since it deals with data in Storage area. Thus, when we use event to store the value of a certain variable in transaction log, local Memory type variable would be preferable to Storage type variable if they hold the same value.

The checker is implemented using Python, and is supported by [python-solidity-parser](https://github.com/ConsenSys/python-solidity-parser).

## Install the Checker

The original source code for the checker is in folder [gas_reducer](./gas_reducer), and we have already packaged the code for your convenience. You can download the package from folder [dist](./dist), using either of the following two ways.

#### whl

click [here](./dist/gas_reducer-0.0.1-py3-none-any.whl) to download gas_reducer-0.0.1-py3-none-any.whl

```
#> pip install gas_reducer-0.0.1-py3-none-any.whl
```
or
```
#> pip3 install gas_reducer-0.0.1-py3-none-any.whl
```

#### tar.gz

click [here](./dist/gas_reducer-0.0.1.tar.gz) to download gas_reducer-0.0.1.tar.gz

```
#> tar -xzvf gas_reducer-0.0.1.tar.gz
#> cd gas_reducer-0.0.1
#> python3 setup.py install
```

## How To Use the Checker
```
#> python3 -m gas_reducer <path_to_contract.sol>
```
or
```
#> python3 -m gas_reducer <path_to_your_project>
```
the output will be:
```
Advice: Use Memory Type Variable Instead of Storage Type Variable in Event to Save Gas
Location:
	 filename: [which file needed to fix]
	 function name: [The function where the problematic event is located]
	 event name: [which event you can improve]
	 variable name: [the name of problematic event logging parameter]
...
```
## Evaluation of the Checker

We applied the checker to the top 200 popular GitHub Solidity projects, and it detected that 35 projects suffered from this issue for their latest versions of code. In total, there are 207 problematic event logging uses. We reported this issue to project owners, and the owners of 9 projects have already confirmed the detected problems. Some of them commented that our finding is quite interesting and can be integrated into the compiler optimization process. This result confirms the usefulness of our checher and suggests that based on our finding, even a simple checker can effectively help for improving the quality of Solidity event logging code. 

https://github.com/OokiTrade/contractsV2/pull/282 <br>
https://github.com/argentlabs/argent-contracts/pull/306 <br>
https://github.com/VenusProtocol/venus-protocol/pull/147 <br>
https://github.com/bnb-chain/bsc-genesis-contract/pull/186 <br>
https://github.com/unlock-protocol/unlock/pull/9565 <br>
https://github.com/smartcontractkit/foundry-starter-kit/pull/12 <br>
https://github.com/Dapp-Learning-DAO/Dapp-Learning/pull/825 <br>
https://github.com/DeFiOptions/DeFiOptions-core/issues/22 <br>
https://github.com/Wonderland-Money/contracts/issues/15 <br>
