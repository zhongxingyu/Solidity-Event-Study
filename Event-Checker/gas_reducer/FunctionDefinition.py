from gas_reducer import SolidityUnit


def retrieveTransferFromContract(contract_node):
    function_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'FunctionDefinition':
            if item['name'].find("transfer") != -1 or item['stateMutability'] == 'payable':
                function_list.append(item)
    return function_list


def IsContainedEmitStatement(function_node):
    result = getEmitStatementFromFunctionDefinition(function_node)
    if len(result) == 0:
        return False
    else:
        return True


def retrieveApproveFromContract(contract_node):
    function_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'FunctionDefinition':
            if "approv" in item['name'] or "Approv" in item['name']:
                function_list.append(item)
    return function_list


def retrieveConstructorFromContract(contract_node):
    function_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'FunctionDefinition':
            if item['name'] == 'constructor':
                function_list.append(item)
    return function_list


def getAllStateVariableDeclarationFromContractDefinition(contract_list):
    state_list = []
    for contract_node in contract_list:
        state_list.append(SolidityUnit.getStateVariableDeclarationFromContractDefinition(contract_node))
    return state_list


def getNameTypeFromStateVariableDeclaration(state_node):
    name = []
    if state_node['variables'] is not None:
        for item in state_node['variables']:
            if 'storageLocation' in item:
                if item['storageLocation'] != 'storage':
                    name.append(item['name'])
            else:
                name.append(item['name'])
    return name


def getAllNameTypeFromStateVariableDeclaration(state_list):
    nameType = []
    for item in state_list:
        temp = getNameTypeFromStateVariableDeclaration(item)
        if temp is not None:
            nameType.extend(temp)
    return nameType


def getEmitStatementFromFunctionDefinition(function_node):
    if len(function_node['body']) == 0:
        return []
    nodes = function_node['body']['statements']
    emit_statements = []
    for item in nodes:
        if item is None:
            continue
        if 'type' not in item:
            continue
        if item['type'] == 'EmitStatement':
            emit_statements.append(item)
        elif item['type'] == 'IfStatement':
            if item['TrueBody'] == ";" or item['FalseBody'] == ";":
                continue
            if item['TrueBody'] is not None and item['TrueBody']['type'] == 'Block':
                nodes.extend(item['TrueBody']['statements'])
            elif item['FalseBody'] is not None and item['FalseBody']['type'] == 'Block':
                nodes.extend(item['FalseBody']['statements'])
        elif item['type'] == 'ForStatement' and item['body']['type'] == 'Block':
            nodes.extend(item['body']['statements'])
        elif item['type'] == 'UncheckedStatement':
            if len(item['body'])!=0 and item['body']['type'] == 'Block':
                nodes.extend(item['body']['statements'])
    return emit_statements


def getVariablesFromEmitStatement(emit_statement):
    variable_list = emit_statement['eventCall']['arguments']
    result = []
    for item in variable_list:
        if item['type'] == 'Identifier':
            result.append(item['name'])
        # elif item['type'] == 'IndexAccess':
        #     variable_list.append(item['base'])
        # elif item['type'] == 'FunctionCall':

    return result


def getAllVariableFromEmitStatementList(emit_statement_list):
    result = []
    for item in emit_statement_list:
        result.append(getVariablesFromEmitStatement(item))
    return result


def getVariableDeclarationStatementFromFunctionDefinition(function_node):
    nodes = function_node['body']['statements']
    variable_statements = []
    for item in nodes:
        if item is None:
            continue
        if 'type' not in item:
            continue
        if item['type'] == 'VariableDeclarationStatement':
            variable_statements.append(item)
        elif item['type'] == 'IfStatement':
            if item['TrueBody'] == ";" or item['FalseBody'] == ";":
                continue
            if item['TrueBody'] is not None and item['TrueBody']['type'] == 'Block':
                nodes.extend(item['TrueBody']['statements'])
            elif item['FalseBody'] is not None and item['FalseBody']['type'] == 'Block':
                nodes.extend(item['FalseBody']['statements'])
        elif item['type'] == 'ForStatement' and item['body']['type'] == 'Block':
            nodes.extend(item['body']['statements'])
        elif item['type'] == 'UncheckedStatement':
            if len(item['body'])!=0 and item['body']['type'] == 'Block':
                nodes.extend(item['body']['statements'])
    return variable_statements


def getParameterVariableFromFunctionDefinition(function_node):
    parameters_list = function_node['parameters']['parameters']
    result = []
    for item in parameters_list:
        if item['type'] == 'Parameter' and item['typeName']['type'] != 'ArrayTypeName' and item['storageLocation'] != 'storage':
            result.append(item['name'])
    return result


def getBinaryOperationFromStatements(statement_node):
    nodes = [statement_node]

    binary_operation_list = []
    binary_variable_list = []

    for item in nodes:

        if item is None:
            continue
        if 'type' not in item:
            continue

        if item['type'] == 'ExpressionStatement':
            if item['expression']['type'] == 'BinaryOperation':
                binary_operation_list.append(item['expression'])
        elif item['type'] == 'IfStatement':
            if item['TrueBody'] == ";" or item['FalseBody'] == ";":
                continue
            if item['TrueBody'] is not None and item['TrueBody']['type'] == 'Block':
                nodes.extend(item['TrueBody']['statements'])
            elif item['FalseBody'] is not None and item['FalseBody']['type'] == 'Block':
                nodes.extend(item['FalseBody']['statements'])
        elif item['type'] == 'ForStatement' and item['body']['type'] == 'Block':
            nodes.extend(item['body']['statements'])
        elif item['type'] == 'VariableDeclarationStatement':
            if item['initialValue'] is not None:
                if item['initialValue']['type'] == 'Identifier':
                    binary_variable_list.append([item['variables'][0]['name'], item['initialValue']['name']])
        elif item['type'] == 'UncheckedStatement':
            if len(item['body'])!=0 and item['body']['type'] == 'Block':
                nodes.extend(item['body']['statements'])

    for item in binary_operation_list:
        if item['left']['type'] == 'IndexAccess':
            node = item['left']['base']
            while node['type'] == 'IndexAccess':
                node = node['base']
            if node['type'] != 'Identifier':
                continue
            left_variable = node['name']
        elif item['left']['type'] == 'Identifier':
            left_variable = item['left']['name']
        else:
            continue

        if item['right']['type'] == 'IndexAccess':
            node = item['right']['base']
            while node['type'] == 'IndexAccess':
                node = node['base']
            if node['type'] != 'Identifier':
                continue
            right_variable = node['name']
        elif item['right']['type'] == 'Identifier':
            right_variable = item['right']['name']
        else:
            continue
        binary_variable_list.append([left_variable, right_variable])

    return binary_variable_list


def getBinaryOperationFromFunctionDefinition(function_node):
    nodes = function_node['body']['statements']
    binary_operation_list = []
    binary_variable_list = []

    for item in nodes:

        if item is None:
            continue
        if 'type' not in item:
            continue

        if item['type'] == 'ExpressionStatement':
            if item['expression']['type'] == 'BinaryOperation':
                binary_operation_list.append(item['expression'])
        elif item['type'] == 'IfStatement':
            if item['TrueBody'] == ";" or item['FalseBody'] == ";":
                continue
            if item['TrueBody'] is not None and item['TrueBody']['type'] == 'Block':
                nodes.extend(item['TrueBody']['statements'])
            elif item['FalseBody'] is not None and item['FalseBody']['type'] == 'Block':
                nodes.extend(item['FalseBody']['statements'])
        elif item['type'] == 'ForStatement' and item['body']['type'] == 'Block':
            nodes.extend(item['body']['statements'])
        elif item['type'] == 'VariableDeclarationStatement':
            if item['initialValue'] is not None:
                if item['initialValue']['type'] == 'Identifier':
                    binary_variable_list.append([item['variables'][0]['name'],item['initialValue']['name']])
        elif item['type'] == 'UncheckedStatement':
            if len(item['body'])!=0 and item['body']['type'] == 'Block':
                nodes.extend(item['body']['statements'])

    for item in binary_operation_list:
        if item['left']['type'] == 'IndexAccess':
            node = item['left']['base']
            while node['type'] == 'IndexAccess':
                node = node['base']
            if node['type'] != 'Identifier':
                continue
            left_variable = node['name']
        elif item['left']['type'] == 'Identifier':
            left_variable = item['left']['name']
        else:
            continue

        if item['right']['type'] == 'IndexAccess':
            node = item['right']['base']
            while node['type'] == 'IndexAccess':
                node = node['base']
            if node['type'] != 'Identifier':
                continue
            right_variable = node['name']
        elif item['right']['type'] == 'Identifier':
            right_variable = item['right']['name']
        else:
            continue
        binary_variable_list.append([left_variable,right_variable])

    return binary_variable_list


def checkVariable(binary_operation_list,variable,temp_typename_list,emit_variable_list):
    flag = False
    for item in binary_operation_list:
        if item[0] == variable:
            if item[1] in temp_typename_list and item[1] not in emit_variable_list:
                flag = True
                break
        elif item[1] == variable:
            if item[0] in temp_typename_list and item[0] not in emit_variable_list:
                flag = True
                break

    return flag