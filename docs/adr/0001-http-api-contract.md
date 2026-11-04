# ADR 0001: Contrato HTTP local versionado

- Status: aceito
- Data: 2026-11-03

## Contexto

O desktop e o backend são processos separados. Sem um contrato explícito,
alterações em filtros, paginação e erros podem quebrar a interface sem
diagnóstico claro.

## Decisão

A API local utilizará o prefixo `/api/v1`.

Respostas de coleção usarão paginação baseada em offset:

```json
{
  "items": [],
  "total": 0,
  "offset": 0,
  "limit": 50
}
```

Erros serão retornados em formato estável:

```json
{
  "error": {
    "code": "validation_error",
    "message": "A entrada é inválida.",
    "details": {}
  }
}
```

O backend não exporá modelos ORM diretamente. Schemas de entrada e saída serão
definidos na camada HTTP e poderão gerar tipos para o frontend em uma etapa
posterior.

## Consequências

- Mudanças incompatíveis exigem uma nova versão do prefixo.
- O frontend pode tratar erros sem depender de mensagens específicas do ORM.
- Offset é simples para a primeira versão local; paginação por cursor pode ser
  adicionada quando houver necessidade mensurável.

## Alternativas rejeitadas

- Expor endpoints sem versão: dificultaria evolução do aplicativo instalado.
- Retornar objetos ORM: acoplaria a API ao modelo de persistência.
- Usar GraphQL inicialmente: adicionaria complexidade sem requisito atual.
