# Continuidade — CorePad Beta Carbon

A linha escolhida pelo proprietário é a **Beta em aparência de fibra de carbono**, sem filete verde superior e com faixa RGB somente na base. Todo o desenvolvimento ativo fica em `beta_blender/`, `development/` e `docs/`.

## Ordem de leitura e autoridade

1. `Especificacao_Produto_Macropad_Biometrico_Gravador_2026-11-21.md`: decisões expressas do proprietário e pendências.
2. `beta_blender/LEIA-ME.md` e `Beta_v1.0.1.blend`: linguagem visual escolhida, materiais refinados e galeria RGB; a 1.0.0 preserva vistas técnicas de geometria.
3. `development/README.md`, `development/VALIDATION.md` e `docs/STATUS.md`: implementação e verificações atuais.
4. `development/hardware/v0.2.0/`: esquema de interface, PCB, BOM e `ARCHITECTURE_REFERENCE.md` com a proposta técnica herdada.
5. `development/mechanical/v0.1.0/`: peças de prototipagem, cuja espessura exploratória difere do modelo visual.
6. `docs/ROADMAP.md`: próximos marcos.

`.old/` contém histórico substituído. Não carregar essa pasta por padrão nem extrair requisitos dela. Consulte apenas para investigar uma decisão antiga. Não restaure o filete verde superior.

## Estado real

- A Beta define aparência; material físico e processo de acabamento ainda precisam ser escolhidos.
- A interface de bancada contém esquema e redes, mas tem 29 conexões não roteadas. Seus conectores recebem chicotes; não são footprints das teclas do produto.
- A principal contém contorno e footprint MCU; esquema completo e roteamento estão pendentes.
- O firmware é um núcleo C portátil testado. O configurador é um editor com simulador, sem transporte USB físico.
- As peças plásticas são sólidos fechados para estudo; fixações, suportes e tolerâncias ainda estão pendentes.
- Gravação, segurança biométrica, FIDO2 e 30 horas de autonomia precisam ser demonstrados em hardware.

## Regras de desenvolvimento

1. Identifique o requisito ou risco que a tarefa resolve.
2. Diferencie requisito aprovado, escolha de engenharia, hipótese e resultado medido.
3. Use documentação primária e registre código exato, URL e data. Não invente pinagem, dimensões ou desempenho.
4. Preserve revisões entregues; crie nova versão `MAJOR.MINOR.PATCH` em cada linha.
5. Execute ERC/DRC quando aplicável e guarde os relatórios. Não liberar fabricação enquanto houver esquema, BOM, roteamento ou integração pendentes.
6. Para Blender, preserve gerador, modelo, renders e validação correspondentes. Renders do README devem representar os arquivos reais e ter legenda de estágio.
7. Mantenha segredos e credenciais fora do microSD e da configuração pública.
8. Atualize `docs/STATUS.md` e `development/VALIDATION.md` quando houver mudança factual.

## Próximas etapas

Fechar pinagem simultânea STM32U5A5, validar USB Audio com microSD em bancada, dimensionar energia/RGB, resolver mudo físico independente, selecionar biometria segura, fechar esquema e BOM da principal, integrar as peças reais, rotear e ensaiar o protótipo.

Ao entregar uma sessão, informe arquivos alterados, decisões, evidências, limitações e próximo passo. Não versionar temporários ou segredos.
