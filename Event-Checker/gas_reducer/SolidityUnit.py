import os
# import difflib
import solidity_parser
import queue


def solidity_parse(path):
    try:
        # print("\t\t compiling " + path)
        source_unit = solidity_parser.parse_file(path)
    except:
        source_unit = None
        # print("parse error!\t" + path)
    return source_unit


def getPragmaDirective(source_unit):
    pragma_list = []
    for child in source_unit['children']:
        if child['type'] == "PragmaDirective":
            pragma_list.append(child)
    return pragma_list


def getImportDirective(source_unit):
    import_list = []
    for child in source_unit['children']:
        if child is None:
            continue
        if child['type'] == 'ImportDirective':
            import_list.append(child)
    return import_list


def getContractDefinition(source_unit):
    contract_list = []
    for child in source_unit['children']:
        if child is None:
            continue
        if child['type'] == 'ContractDefinition':
            if child['kind'] == 'contract':
                contract_list.append(child)
    return contract_list


def getFunctionDefinitionFromContractDefinition(contract_node):
    function_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'FunctionDefinition':
            function_list.append(item)
    return function_list


def getStateVariableDeclarationFromContractDefinition(contract_node):
    state_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'StateVariableDeclaration':
            state_list.append(item)
    return state_list


def getBaseContractsFromContractDefinition(contract_node):
    result = []
    for base_item in contract_node['baseContracts']:
        result.append(base_item['baseName']['namePath'])
    return result


def repairNewPath(absolute_path, path):
    if './' not in path:
        return path

    path_list = path.split("/")
    absolute_path_list = absolute_path.split("/")
    absolute_path_list.pop()
    for i in range(0, len(path_list)):
        item = path_list[i]
        if item == "..":
            absolute_path_list.pop()
        elif item == ".":
            continue
        else:
            break
    result = "/".join(absolute_path_list) + "/" + "/".join(path_list[i:])
    return result


def getAllPathFromImportDirective(absolute_path, import_list):
    relative_path_list = queue.Queue()
    absolute_path_list = []
    for import_node in import_list:
        relative_path_list.put(import_node['path'])

    while relative_path_list.qsize() > 0:
        path_item = repairNewPath(absolute_path, relative_path_list.get())
        absolute_path_list.append(path_item)
        if not os.path.exists(path_item):
            continue
        source_unit = solidity_parse(path_item)
        if source_unit is None:
            continue
        import_list = getImportDirective(source_unit)
        for import_node in import_list:
            relative_path_list.put(import_node['path'])

    return absolute_path_list


def IsContainedERC20OrERC2771Context(path_list):
    for item in path_list:
        if "@openzeppelin" in item:
            if "ERC20.sol" in item or "ERC2771Context.sol" in item or "Context.sol" in item:
                return True

    return False


def getEventDefinitionFromContractDefinition(contract_node):
    event_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'EventDefinition':
            event_list.append(item)
    return event_list


def getVariableFromEventDefinition(event_node):
    name = event_node['name']
    parameter = []
    for item in event_node['parameters']['parameters']:
        if item['name'] == None:
            continue
        parameter.append(item['name'])
    return [name, parameter]


def getAllVariableFromEventDefinition(event_list):
    result = []
    for event_node in event_list:
        result.append(getVariableFromEventDefinition(event_node))
    return result


def getEventDefinitionFromList(event_name, event_list):
    for event in event_list:
        if event_name == event[0]:
            return event[1]


def calculateSimilarity(src_list, target_list):
    if len(src_list) != len(target_list):
        return False
    result = []
    for src_node in src_list:
        similarity = 0
        for target_node in target_list:
            temp = difflib.SequenceMatcher(None, src_node, target_node).quick_ratio()
            if temp > similarity:
                similarity = temp
        result.append(similarity)

    for item in result:
        if item < 0.9:
            return False

    for i in range(0,len(src_list)):
        similarity = difflib.SequenceMatcher(None,src_list[i], target_list[i]).quick_ratio()
        if similarity < 0.9:
            return True

    return False


def IsOrderError(src_list, target_list):
    if len(src_list) != len(target_list):
        return False

    for src_node in src_list:
        if src_node not in target_list:
            return False

    for i in range(0,len(src_list)):
        if src_list[i] != target_list[i]:
            return True

    return False





