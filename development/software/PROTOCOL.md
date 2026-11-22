# Configuração pública v1

O configurador é desktop em Python/Tkinter. A implementação atual aplica configurações a um simulador em memória e salva/carrega arquivos JSON UTF-8. Transporte USB físico e persistência no dispositivo ainda não existem.

Formato:

```json
{"version":1,"rgb":{"color":"#00ff00","brightness":32,"enabled":false},"macros":[["","","","","","","","",""],["","","","","","","","",""]]}
```

Somente comandos `get_config` e `set_config` são aceitos pelo simulador. `set_config` valida toda a estrutura antes de alterar estado. São 2 × 9 macros comuns, até 256 caracteres Unicode cada. O MCU precisará reservar até 1.024 bytes UTF-8 por macro mais terminador e metadados. Nenhuma operação pública autentica biometria, libera a terceira camada ou exporta segredos.

A próxima implementação deve usar canal USB autenticado quando aplicável, versionamento de mensagens, comprimento limitado, CRC/checagem de integridade, IDs, timeout e confirmação de escrita transacional. JSON é o formato de intercâmbio do configurador; não foi decidido que será o formato de armazenamento do MCU.

RGB permanece desligado no padrão de desenvolvimento para facilitar ensaios de consumo. A gravação autônoma deve declarar se a faixa estava ligada e em que brilho. O núcleo C desliga RGB ao entrar em bateria baixa.

Textos Unicode no arquivo não provam digitação correta pelo HID. Tradutor de layout Windows/macOS, acentuação e envio de atalhos ainda precisam de implementação e testes.
