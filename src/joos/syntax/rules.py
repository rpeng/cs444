from joos.syntax import *

rules_map = {
    # ----- Base -----
    'CompilationUnit': CompilationUnit,
    'Type': Type,  # abstract
    'ArrayType': ArrayType,
    'ClassOrInterfaceType': ClassOrInterfaceType,
    'PrimitiveType': PrimitiveType,
    'Name': Name,
    'Literal': Literal,
    '2147483648': Literal,

    # ----- Decl -----
    'PackageDeclaration': PackageDecl,
    'ImportDeclaration': ImportDecl,
    'TypeDeclaration': TypeDecl,  # abstract
    'ClassDeclaration': ClassDecl,
    'InterfaceDeclaration': InterfaceDecl,
    'MethodDeclaration': MethodDecl,
    'MethodHeader': MethodHeader,
    'FieldDeclaration': FieldDecl,
    'ConstructorDeclaration': ConstructorDecl,
    'VariableDeclarator': VariableDeclarator,
    'LocalVariableDeclaration': LocalVarDecl,
    'FormalParameter': Parameter,

    # ----- Expression -----
    'Expression': Expression,  # abstract

    'AssignmentExpression': AssignmentExpression,
    'Assignment': AssignmentExpression,

    'ConditionalOrExpression': BinaryExpression,
    'ConditionalAndExpression': BinaryExpression,
    'InclusiveOrExpression': BinaryExpression,
    'AndExpression': BinaryExpression,
    'EqualityExpression': BinaryExpression,
    'RelationalExpression': BinaryExpression,
    'AdditiveExpression': BinaryExpression,
    'MultiplicativeExpression': BinaryExpression,

    'UnaryExpression': UnaryExpression,
    'UnaryExpressionOrMaxInt': UnaryExpression,
    'UnaryExpressionNotPlusMinus': UnaryExpression,

    'CastExpression': CastExpression,
    'FieldAccess': FieldAccess,
    'ArrayAccess': ArrayAccess,

    'Primary': Primary,  # Abstract
    'PrimaryNoNewArray': Primary,

    'this': ThisExpression,
    'ArrayCreationExpression': ArrayCreationExpression,
    'StatementExpression': StatementExpression,  # Abstract
    'ClassInstanceCreationExpression': ClassInstanceCreationExpression,
    'MethodInvocation': MethodInvocation,

    # ----- Statement -----
    'Statement': Statement,  # Abstract
    'ExpressionStatement': Statement,
    'StatementWithoutTrailingSubstatement': Statement,
    'StatementNoShortIf': Statement,
    'EmptyStatement': Statement,

    'Block': Block,

    'IfThenElseStatement': IfThenElseStatement,
    'IfThenStatement': IfThenElseStatement,
    'IfThenElseStatementNoShortIf': IfThenElseStatement,

    'WhileStatement': WhileStatement,
    'WhileStatementNoShortIf': WhileStatement,

    'ForStatement': ForStatement,
    'ForStatementNoShortIf': ForStatement,

    'LocalVariableDeclarationStatement': LocalVarDeclStatement,  # Abstract
}
