# Evolution of Event Logging Code in Solidity Projects

## Overall

Event logging code is modified in a significant number (11.83%) of all the committed revisions, and its average churn rate is nearly the same as that of the entire code.
Overall, event logging code is being continuously and actively modified by developers, suggesting that Solidity developers are actively maintaining event logging code like other non-logging code for software functionality.

In particular, there exists a significant percentage (with lower bound being 10.64%) of event logging code modifications that are independent of other code changes (termed `independent event logging code modification`), suggesting that the current developer practices of using Solidity event feature are not good enough and some developers tend to use event logging feature in a subjective and arbitrary way. After detecting the event use problems, developers take efforts to address them as after-thoughts. 

## Independent Event Logging Code Modification

We further study the details of independent event logging code modifications. To accomplish this, we randomly sample 419 independent event logging code modifications,  which achieves 99% confidence level and ±5% confidence interval. For these sampled modifications, we examine developers’ commit messages, source code, together with the event logging code modifications to understand the modifications. Each modification is checked by two authors of the paper. If they cannot clearly understand the reason or have disagreements with the reason for some modifications, we always conservatively classify them as the “unknown” category when presenting our results. 

The manual analysis suggests that the 419 modifications can be divided into 5 categories in general, including `Parameter Change`, `Addition`, `Deletion`, `Move`, and `Replacement`. The folders [Parameter_Change](./Parameter_Change), [Addition](./Addition), [Deletion](./Deletion), [Move](./Move), and [Replacement](./Replacement) respectively contain modifications that fall into these 5 categories. Inside each of these 5 folders, we give the particular meaning of the corresponding change category and the underlying reasons for modifications in that change category. For each specific reason, we organize modifications arisen because of it into a table and give the snippet of the original event logging code changes for each modification. 

For three modifications, they do not fit with the 5 categories mentioned above, and we put them into the folder [Others](./Others).
