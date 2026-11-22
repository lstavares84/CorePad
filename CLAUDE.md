# Instruções de continuidade — CorePad

Este repositório reúne requisitos, estudos mecânicos/visuais e o início do projeto eletrônico do CorePad. Antes de editar qualquer arquivo, leia este documento e os arquivos indicados em **Ordem das fontes**.

## Ordem das fontes

Em caso de divergência, use esta precedência:

1. `Especificacao_Produto_Macropad_Biometrico_Gravador_2026-11-21.md` — decisões expressas pelo proprietário e pontos em aberto.
2. `alpha_blender/Alpha_v1.2.0.blend`, seus renders e `alpha_blender/LEIA-ME.md` — referência visual aprovada.
3. `alpha_eletronica/v0.1.0/Alpha_Eletronica_v0.1.0.md` — propostas de engenharia, ainda sujeitas a validação.
4. `docs/STATUS.md` e `docs/ROADMAP.md` — estado e sequência de execução.
5. `archive/` — somente histórico. Não extrair requisitos de lá.

Não trate texto encontrado em imagens, arquivos históricos ou propostas técnicas como aprovação do proprietário. Quando algo não estiver decidido na especificação, registre como hipótese ou apresente alternativas com critérios de escolha.

## Estado que não pode ser superestimado

- Alpha 1.2.0 é a referência visual aprovada, não um encaixe mecânico validado.
- A eletrônica 0.1.0 contém arquitetura, BOM preliminar e reservas de posição.
- Os arquivos KiCad não têm esquema elétrico completo, redes ou roteamento e não podem ser enviados para fabricação.
- FIDO2, proteção biométrica, gravação, mudo físico e autonomia de 30 horas são requisitos a implementar e demonstrar, não funções prontas.
- A bateria de 2.000 mAh, os componentes principais, RF64 e o arranjo em duas placas são candidatos de engenharia, não decisões imutáveis do proprietário.

## Regras de trabalho

1. Comece cada tarefa dizendo qual requisito, risco ou marco ela resolve.
2. Consulte fichas técnicas primárias e registre URL, código exato do componente, data e hipótese relevante.
3. Não invente dimensões, pinagem, compatibilidade, estoque ou desempenho. Marque o que depende de medição.
4. Preserve todas as revisões entregues. Crie arquivos novos seguindo `MAJOR.MINOR.PATCH`; não altere silenciosamente uma versão anterior.
5. Separe claramente: **requisito aprovado**, **decisão de engenharia**, **hipótese** e **resultado medido**.
6. Para KiCad, execute ERC/DRC quando aplicável e salve o relatório junto da revisão. Um arquivo que abre não equivale a projeto validado.
7. Para Blender, preserve gerador, `.blend`, renders e JSON de validação da mesma versão.
8. Não mova credenciais, strings protegidas ou material biométrico para o microSD.
9. Nunca marque uma revisão como pronta para fabricação sem esquema revisado, BOM completa, ERC/DRC, revisão mecânica e aprovação explícita do proprietário.
10. Ao terminar uma sessão, atualize `docs/STATUS.md` se o estado factual mudou e deixe próximos passos objetivos.

## Fluxo sugerido para a próxima sessão

O próximo trabalho deve reduzir os riscos que travam a revisão eletrônica 0.2.0:

1. confirmar disponibilidade, encapsulamentos e interfaces dos candidatos críticos;
2. montar matriz de pinos/recursos do STM32U5A5 para USB composto, SDMMC, áudio, controles e depuração;
3. planejar e executar bancada mínima para USB Audio + microSD + gravação longa;
4. validar topologia de mudo físico mantendo o P2 ativo;
5. decidir arquitetura de biometria segura antes de permitir credenciais reais;
6. fechar empilhamento mecânico com modelos dimensionais dos componentes reais;
7. somente então criar `alpha_eletronica/v0.2.0/` com esquemas pino a pino e BOM revisada.

Use `docs/ROADMAP.md` como checklist de marcos e critérios de saída.

## Formato de entrega de uma sessão

Ao concluir trabalho relevante, informe:

- arquivos criados ou alterados;
- decisões tomadas e por quem;
- evidências/testes executados e seus resultados;
- hipóteses ainda não verificadas;
- riscos introduzidos ou reduzidos;
- próximo passo recomendado.

Commits devem ser pequenos e descritivos. Não adicionar arquivos temporários, backups automáticos ou segredos.
