from joos.syntax import *

rules_map = {
    # ----- Base -----
    'CompilationUnit': CompilationUnit,
    'Type': Type,  # abstract
    'ReferenceType': ReferenceType,  # abstract
    'ArrayType': ArrayType,
    'ClassOrInterfaceType': ClassOrInterfaceType,
    'PrimitiveType': PrimitiveType,
    'void': VoidType,
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
    'PrimaryNoNewArray': ParensExpression,
    'FieldAccess': FieldAccess,
    'ArrayAccess': ArrayAccess,

    'Primary': Primary,  # Abstract

    'this': ThisExpression,
    'ArrayCreationExpression': ArrayCreationExpression,
    'StatementExpression': StatementExpression,
    'NameExpression': NameExpression,
    'ClassInstanceCreationExpression': ClassInstanceCreationExpression,
    'MethodInvocation': MethodInvocation,

    # ----- Statement -----
    'Statement': Statement,  # Abstract
    'ExpressionStatement': Statement,
    'StatementWithoutTrailingSubstatement': Statement,
    'StatementNoShortIf': Statement,
    'ReturnStatement': ReturnStatement,
    'EmptyStatement': EmptyStatement,

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
