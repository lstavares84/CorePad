# CorePad

Macropad USB-C compacto com nove teclas em matriz 3 × 3, autenticação biométrica, controle de áudio e gravação de reuniões. **CorePad** é o nome do produto; **Alpha** é a proposta visual escolhida e identifica os arquivos de modelagem.

![CorePad Beta 1.0.0](beta_blender/Beta_v1.0.0_frente_esquerda.png)

## Onde o projeto está

- **Especificação vigente:** [versão 0.7](Especificacao_Produto_Macropad_Biometrico_Gravador_2026-11-21.md), consolidada em 21/11/2026 e atualizada em 22/11/2026.
- **Proposta visual atual:** [`Beta_v1.0.0.blend`](beta_blender/Beta_v1.0.0.blend), em estilo fibra de carbono, sem filete superior e com faixa RGB configurável somente na base.
- **Linha Alpha preservada:** [`Alpha_v1.3.0.blend`](alpha_blender/Alpha_v1.3.0.blend) mantém o histórico visual anterior.
- **Desenvolvimento integrado Beta:** [`development/`](development/README.md) contém firmware C testado, configurador desktop com simulador, interface de bancada KiCad com redes, peças STL e BOM por bloco. A placa principal e a integração física continuam em desenvolvimento.
- **Eletrônica:** revisão exploratória [`0.1.0`](alpha_eletronica/v0.1.0/Alpha_Eletronica_v0.1.0.md), ainda sem esquema elétrico completo, redes ou trilhas.
- **Próximo marco:** validar a arquitetura em bancada e produzir a revisão eletrônica 0.2.0 com pinagem, esquemas e BOM fechada para protótipo.

> Os arquivos KiCad atuais são estudos de posicionamento. **Não estão liberados para fabricação.** A meta de 30 horas de gravação com bateria interna depende de medição em protótipo.

## Começar pelo Claude

Abra este repositório no Claude Code e peça para ele ler [`CLAUDE.md`](CLAUDE.md) antes de propor ou alterar qualquer coisa. O arquivo contém a ordem das fontes, limites do estado atual, convenções de versionamento e o fluxo esperado para cada sessão.

Depois consulte:

1. [`docs/STATUS.md`](docs/STATUS.md) — estado verificável e principais riscos;
2. [`docs/ROADMAP.md`](docs/ROADMAP.md) — etapas, entregáveis e critérios de saída;
3. [especificação do produto](Especificacao_Produto_Macropad_Biometrico_Gravador_2026-11-21.md) — requisitos aprovados e pontos ainda abertos;
4. [estudo eletrônico 0.1.0](alpha_eletronica/v0.1.0/Alpha_Eletronica_v0.1.0.md) — arquitetura proposta e fontes técnicas.

## Estrutura

| Caminho | Conteúdo | Autoridade |
|---|---|---|
| `Especificacao_Produto_...md` | Requisitos e decisões do produto | Fonte principal do escopo |
| `alpha_blender/` | Modelos, geradores, validações e renders Alpha | Referência visual aprovada |
| `beta_blender/` | Design Beta em fibra de carbono, sem filete superior | Proposta visual atual |
| `development/` | Hardware, firmware, configurador, peças e BOM Beta | Desenvolvimento de protótipo; consulte os limites por entrega |
| `alpha_eletronica/` | Arquitetura, BOM, KiCad, cálculos e verificações | Engenharia preliminar |
| `docs/` | Status operacional e roteiro de desenvolvimento | Guia de continuidade |
| `archive/` | Estudos descartados, imagens geradas e versões históricas | Consulta histórica; não usar como requisito |

## Regras de versão

- Blender: `Alpha_vMAJOR.MINOR.PATCH.*`.
- Blender Beta: `Beta_vMAJOR.MINOR.PATCH.*`.
- Eletrônica: diretório `alpha_eletronica/vMAJOR.MINOR.PATCH/`, com numeração independente.
- Nunca sobrescrever uma revisão entregue; criar a próxima versão e preservar a anterior.
- Atualizar `README.md`, `docs/STATUS.md` e os arquivos de verificação ao fechar um marco.

Projeto privado e em desenvolvimento. Nenhuma licença de distribuição foi concedida.
