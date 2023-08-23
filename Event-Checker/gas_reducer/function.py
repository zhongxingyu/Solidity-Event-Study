from gas_reducer import Rules
from gas_reducer import SolidityUnit

def scan(absolute_path):
    source_unit = SolidityUnit.solidity_parse(absolute_path)
    if source_unit is None:
        return -1
    contract_list = SolidityUnit.getContractDefinition(source_unit)
    # Rules.emitChangeParameter_MetaTransaction(absolute_path, source_unit)

    for contract_node in contract_list:
        # Rules.emitAdd_AfterTransfer(contract_node)
        # Rules.emitAdd_AfterApprove(contract_node)
        # Rules.emitAdd_AfterConstruct(contract_node)
        Rules.emitChangeParameter_Gas(absolute_path, contract_node)
        # Rules.emitChangeParameter_Version(contract_node)
        # Rules.emitSwapOrder(contract_node)

    return 1