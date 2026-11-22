# Roteiro de desenvolvimento

Este roteiro organiza a evolução do CorePad por evidências. Datas e compras dependem de decisões do proprietário e da disponibilidade dos componentes.

## Marco 1 — Fechar viabilidade da arquitetura

**Objetivo:** provar que os blocos críticos funcionam juntos antes de desenhar a placa.

- [ ] Confirmar códigos, encapsulamentos, status de ciclo de vida e disponibilidade dos componentes críticos.
- [ ] Criar matriz de pinos e recursos do STM32U5A5.
- [ ] Confirmar composição USB: teclado, áudio, configuração, armazenamento e futura autenticação.
- [ ] Testar USB Audio simultâneo com escrita SDMMC/microSD.
- [ ] Gravar arquivo longo, medir pausas máximas e verificar recuperação após falha.
- [ ] Medir consumo por bloco e revisar bateria/meta de 30 horas.
- [ ] Dimensionar a faixa RGB da base, seu difusor e consumo por brilho/cor.
- [ ] Prototipar o mudo físico e confirmar que o P2 continua ativo.
- [ ] Escolher caminho de biometria com comunicação autenticada ou mitigação equivalente.

**Critério de saída:** matriz de recursos revisada, relatórios de bancada reproduzíveis e arquitetura atualizada sem bloqueio conhecido.

## Marco 2 — Eletrônica 0.2.0

**Objetivo:** produzir esquemas completos e uma BOM coerente para revisão técnica.

- [ ] Criar `alpha_eletronica/v0.2.0/` sem sobrescrever 0.1.0.
- [ ] Elaborar esquemas pino a pino de alimentação, MCU, USB, áudio, microSD, segurança, biometria e interface.
- [ ] Dimensionar passivos, relógios, filtros, proteções ESD e pontos de teste.
- [ ] Fechar conectores entre placas e estratégia de programação/depuração.
- [ ] Atualizar BOM com fabricante, código, encapsulamento, alternativa e fonte primária.
- [ ] Executar ERC e revisão por checklist.

**Critério de saída:** zero erro ERC não justificado, BOM completa para protótipo e revisão independente registrada.

## Marco 3 — Mecânica e PCB 0.3.0

**Objetivo:** integrar placas e componentes reais à carcaça sem colisões.

- [ ] Importar modelos 3D certificados dos componentes selecionados.
- [ ] Fechar empilhamento, tolerâncias, fixações, bateria, dutos acústicos e acesso aos conectores.
- [ ] Atualizar a Alpha em nova versão, preservando 1.2.0.
- [ ] Modelar a faixa RGB no perímetro inferior, com emissão difusa para a mesa e sem iluminação sob as teclas.
- [ ] Posicionar e rotear PCB com stack-up do fabricante.
- [ ] Executar DRC, revisão de retorno de corrente, USB, áudio, energia e segurança.
- [ ] Gerar pacote de fabricação somente após aprovação explícita.

**Critério de saída:** revisão mecânica aprovada, DRC limpo/justificado e pacote de protótipo rastreável.

## Marco 4 — Firmware mínimo e protótipo EVT

**Objetivo:** demonstrar as funções essenciais no primeiro hardware.

- [ ] Boot seguro, atualização assinada e recuperação de desenvolvimento.
- [ ] Teclado USB, camadas, LEDs e configuração persistente.
- [ ] Configuração de cor e desligamento da faixa RGB pelo software, sem recompilar o firmware.
- [ ] Áudio USB, P2, microfones e mudo físico.
- [ ] Estados exclusivos Arquivos/Gravação e fechamento robusto do arquivo.
- [ ] Medição de energia e encerramento seguro em bateria baixa.
- [ ] Testes de 30 horas, falha de energia, cartão cheio e retirada de USB.

**Critério de saída:** relatório EVT com resultados, falhas reproduzíveis e revisão priorizada.

## Marco 5 — Segurança, FIDO2 e experiência

**Objetivo:** permitir uso seguro e repetível das funções protegidas.

- [ ] Modelo de ameaça e provisionamento do elemento seguro.
- [ ] Cadeia biométrica autenticada, bloqueio por tentativas e recuperação.
- [ ] CTAP/FIDO2 com confirmação física e testes entre sistemas.
- [ ] Fluxo de textos longos e português/acentos em Windows e macOS.
- [ ] Ferramenta de configuração sem recompilar firmware.
- [ ] Interface de escolha da cor da faixa RGB e persistência da preferência no aparelho.
- [ ] Exportação de gravações para transcrição e ata.

**Critério de saída:** testes de segurança e interoperabilidade documentados, sem credenciais reais antes da aprovação.

## Marco 6 — DVT e preparação de produção

**Objetivo:** transformar o protótipo funcional em produto repetível.

- [ ] Ensaios acústicos, térmicos, autonomia, ESD/EMC e vida útil dos controles.
- [ ] Revisão DFM/DFA e cadeia de fornecimento.
- [ ] Plano de testes de fábrica e provisionamento seguro.
- [ ] Documentação de uso, atualização e recuperação.
- [ ] Decisão de certificações e mercados-alvo.

**Critério de saída:** requisitos verificados, riscos residuais aceitos e liberação formal de produção.
