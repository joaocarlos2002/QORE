# ADR 0002: Autenticação efêmera da API local

- Status: aceito
- Data: 2026-11-03

## Contexto

O FastAPI precisa aceitar chamadas do frontend Tauri sem transformar a API em
um serviço acessível por outros processos da rede local. O endereço de loopback
limita a rede, mas não autentica quem está fazendo a chamada.

## Decisão

Cada inicialização do backend gerará um token aleatório criptograficamente
seguro. O processo Tauri receberá o token por um canal local fora da URL e o
enviará no cabeçalho:

```text
Authorization: Bearer <token>
```

O token:

- terá validade somente durante o processo atual;
- será mantido apenas em memória;
- não será escrito em logs;
- será rejeitado quando ausente, inválido ou após o encerramento do backend.

O backend escutará exclusivamente em `127.0.0.1`. CORS será restrito à origem
do frontend empacotado e não será usado como mecanismo de autenticação.

## Consequências

- Reiniciar o aplicativo invalida tokens anteriores.
- O ciclo de vida Tauri-backend precisa transportar o token com segurança.
- Testes poderão injetar um token conhecido sem depender de segredo persistido.
- Não haverá autenticação multiusuário nesta fase.

## Alternativas rejeitadas

- Sem autenticação: permitiria chamadas locais não autorizadas.
- Token persistente em arquivo: aumentaria o impacto de cópia ou vazamento.
- Senha fixa no código: não oferece rotação nem proteção adequada.
