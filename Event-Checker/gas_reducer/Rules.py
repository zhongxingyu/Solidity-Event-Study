from gas_reducer import FunctionDefinition
from gas_reducer import SolidityUnit


def emitAdd_AfterTransfer(contract_node):
    function_list = FunctionDefinition.retrieveTransferFromContract(contract_node)
    for function_node in function_list:
        if not FunctionDefinition.IsContainedEmitStatement(function_node):
            print("Advice: Please insert event after transaction")
            print("\tLocation: function " + function_node['name'])


def emitAdd_AfterApprove(contract_node):
    function_list = FunctionDefinition.retrieveApproveFromContract(contract_node)
    for function_node in function_list:
        if not FunctionDefinition.IsContainedEmitStatement(function_node):
            print("Advice: Please insert event after authorizing")
            print("\tLocation: function " + function_node['name'])


def emitAdd_AfterConstruct(contract_node):
    function_list = FunctionDefinition.retrieveConstructorFromContract(contract_node)
    for function_node in function_list:
        if not FunctionDefinition.IsContainedEmitStatement(function_node):
            print("Advice: Please insert event in constructor to record the owner")
            print("\tLocation: function " + function_node['name'])


def emitChangeParameter_Gas(absolute_path, contract_node):
    # Get all global variables
    state_variable_list = SolidityUnit.getStateVariableDeclarationFromContractDefinition(contract_node)
    state_typeName_list = FunctionDefinition.getAllNameTypeFromStateVariableDeclaration(state_variable_list)

    function_list = SolidityUnit.getFunctionDefinitionFromContractDefinition(contract_node)
    for function_node in function_list:
        emit_statement_list = FunctionDefinition.getEmitStatementFromFunctionDefinition(function_node)
        if len(emit_statement_list) == 0:
            continue
        function_name = function_node['name']
        # Get all temp variable
        temp_variable_list = FunctionDefinition.getVariableDeclarationStatementFromFunctionDefinition(function_node)
        temp_typename_list = FunctionDefinition.getAllNameTypeFromStateVariableDeclaration(temp_variable_list)
        temp_typename_list.extend(FunctionDefinition.getParameterVariableFromFunctionDefinition(function_node))
        # Get all variable in emit
        binary_operation_list = []

        for statement_node in function_node['body']['statements']:
            if statement_node == ";" or statement_node is None:
                continue
            if statement_node['type'] != 'EmitStatement':
                binary_operation_list.extend(FunctionDefinition.getBinaryOperationFromStatements(statement_node))
            else:
                emit_variable_list = FunctionDefinition.getVariablesFromEmitStatement(statement_node)
                for variable in emit_variable_list:
                    if variable not in temp_typename_list and variable in state_typeName_list:
                        if FunctionDefinition.checkVariable(binary_operation_list, variable, temp_typename_list, emit_variable_list):
                            print("Advice: Use Memory Type Variable Instead of Storage Type Variable in Event to Save Gas")
                            print("Location:\n\t filename: " + absolute_path + "\n\t function name: " + function_node['name'] + "\n\t event name: " + statement_node['eventCall']['expression']['name'] + "\n\t variable name: " + variable + "\n")


def emitChangeParameter_MetaTransaction(absolute_path, source_unit):
    import_list = SolidityUnit.getImportDirective(source_unit)
    path_list = SolidityUnit.getAllPathFromImportDirective(absolute_path, import_list)
    if SolidityUnit.IsContainedERC20OrERC2771Context(path_list):
        contract_list = SolidityUnit.getContractDefinition(source_unit)
        for contract_node in contract_list:
            function_list = SolidityUnit.getFunctionDefinitionFromContractDefinition(contract_node)
            for function_node in function_list:
                emit_statement_list = FunctionDefinition.getEmitStatementFromFunctionDefinition(function_node)
                if len(emit_statement_list) == 0:
                    continue
                for item in emit_statement_list:
                    arguments = item['eventCall']['arguments']
                    for node in arguments:
                        if node['type'] == 'MemberAccess' and node['expression']['name'] == 'msg' and node['memberName'] == 'sender':
                            print("Advice: you should use _msgSender() to replace msg.sender ")
                            print("\tLocation: function " + function_node['name'])


def emitChangeParameter_Version(contract_node):
    function_list = SolidityUnit.getFunctionDefinitionFromContractDefinition(contract_node)
    for function_node in function_list:
        emit_list = FunctionDefinition.getEmitStatementFromFunctionDefinition(function_node)
        for item in emit_list:
            arguments = item['eventCall']['arguments']
            for node in arguments:
                if node['type'] == 'MemberAccess' and node['expression']['name'] == 'this':
                    print("Advice: you should use address(this) instead of this.")
                    print("\tLocation: function " + function_node['name'])


def emitSwapOrder(contract_node):
    event_list = SolidityUnit.getEventDefinitionFromContractDefinition(contract_node)
    event_content_list = SolidityUnit.getAllVariableFromEventDefinition(event_list)
    if len(event_content_list) == 0:
        return 0
    function_list = SolidityUnit.getFunctionDefinitionFromContractDefinition(contract_node)
    for function_node in function_list:
        emit_list = FunctionDefinition.getEmitStatementFromFunctionDefinition(function_node)
        if len(emit_list) == 0:
            continue

        for emit_node in emit_list:
            emit_name = emit_node['eventCall']['expression']['name']
            parameter = []
            for item in emit_node['eventCall']['arguments']:
                if item['type'] == 'Identifier':
                    parameter.append(item['name'])
            event = SolidityUnit.getEventDefinitionFromList(emit_name, event_content_list)
            if SolidityUnit.calculateSimilarity(parameter, event):
                print("Advice: The order of variables recorded in emit should be consistent with the event definition")
                print("\tLocation: function " + function_node['name'])


