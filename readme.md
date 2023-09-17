# Solidity-Event-Logging-Study

## What is this repository? 

This repository serves as the replication package for our ESEC/FSE 2023 paper **"Understanding Solidity Event Logging Practices in the Wild"** (https://arxiv.org/pdf/2308.12788.pdf). 

Writing logging messages is a well-established conventional programming practice, and it is of enormous importance for a wide variety of software development activities. The logging mechanism in Solidity programming is enabled by the high-level event feature, but up to now there lacks study for understanding Solidity event logging practices in the wild. To fill this gap, we in this paper provide the first quantitative characteristic study of the current Solidity event logging practices using 2,915 popular Solidity projects hosted on GitHub. The study methodically explores the pervasiveness of event logging, the goodness of current event logging practices, and in particular the reasons for event logging code evolution, and delivers 8 original and important findings. The findings notably include the existence of a significant percentage of event logging code modifications that are independent of other non-event logging code changes, and the underlying reasons for different categories of independent event logging code modifications are diverse (for instance, bug fixing and gas saving). We additionally give the implications of our findings, and these implications can enlighten developers, researchers, tool builders, and language designers to improve the event logging practices. To illustrate the potential benefits of our study, we develop a proof-of-concept checker on top of one of our findings and the checker effectively detects problematic event logging code that consumes extra gas in 35 popular GitHub projects and 9 project owners have already confirmed the detected issues. 

This repository contains the collected large scale data about density of event logging code, evolution of event logging code in particular our manual analysis of the characteristics of independent event logging code modifications, and our tool for checking problematic event logging parameter in order to save gas.

```
@inproceedings{fse-solidity-logging,
  title={Understanding Solidity Event Logging Practices in the Wild},
  author={Li, Lantian and Liang, Yejian and Liu, Zhihao and Yu, Zhongxing},
  url = {https://arxiv.org/pdf/2308.12788.pdf},
  booktitle={Proceedings of the 31th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering},
  year={2023},
  location = {San Fransisco, USA},
  series = {ESEC/FSE 2023}
}
```

## Structure of this repository

The repository contains three folders: Event-Density, Event-Evolution, and Event-Checker.

- [Event-Density](./Event-Density) contains the raw data about event use per project and per LOC (lines of code) for each of the studied 2,915 Solidity projects. 
- [Event-Evolution](./Event-Evolution) contains the snippets of the original event logging code changes for 419 independent event logging code modifications and our manual analysis of the categories and reasons for these modification.
- [Event-Checker](./Event-Checker) contains the source code for the tool and the instructions on how to install and use the tool. 

Inside each folder, we give more detailed descriptions of the content it contains.  


