# CorePad — Caderno de Engenharia Rev. A

O [PDF A3 paisagem](CorePad_Caderno_de_Engenharia_Rev_A.pdf) consolida o estado verificável do CorePad Beta Carbon em 22/11/2026. É uma **linha de base de engenharia, sem liberação para fabricar**. Onde faltam circuitos, componentes, tolerâncias, procedimentos e ensaios, o documento mostra “A DEFINIR” e aponta responsável funcional e próximo passo. A seção de fontes identifica arquivos do repositório; o [manifesto digital](source_manifest.json) guarda seus SHA-256.

A apresentação segue o sistema “Metrologia Luminosa” fornecido no pedido: A3, margens de 16 mm, grade de pontos, régua milimétrica, fundo claro e divisórias escuras. As sete fontes livres foram obtidas da [biblioteca Google Fonts](https://github.com/google/fonts), congeladas em pesos estáticos, incorporadas ao PDF e acompanhadas das licenças OFL em `fonts/`. Todos os renders usados vêm dos arquivos do projeto.

O [relatório final](relatorio_final.md) registra páginas, tamanho, intervalos das seções, tamanhos de fonte e pendências. O [relatório de QA](relatorio_qa.json) registra as páginas renderizadas, incorporação de fontes e checagem de texto fora do papel. As [prévias](previews/) incluem 37 páginas de amostra e quatro folhas de contato.

O [prompt de origem](prompt_origem.txt) está preservado como anexo de reprodutibilidade do sistema visual e do sumário pedido.

## Reproduzir

Na raiz do repositório:

```sh
python3 docs/engineering/Rev_A/prepare_fonts.py
python3 docs/engineering/Rev_A/build_caderno.py
uv run --with pymupdf python docs/engineering/Rev_A/render_verify.py
```

Dependências: Python com `reportlab`, `fontTools`, `requests`, `Pillow`; `uv` e Poppler (`pdftoppm`, `pdffonts`) para QA. Os arquivos de fonte estáticos já estão versionados; executar `prepare_fonts.py` novamente só quando for deliberadamente atualizá-los, pois uma versão nova pode alterar paginação.

## Limite de uso

O caderno não contém esquema principal completo, Gerbers, CPL, BOM de compra, desenho mecânico liberado, firmware gravável ou plano de testes de produção validado. A montagem STEP e o PDF descrevem o **estado atual do projeto**, não instruções suficientes para uma fábrica construir o produto sem novas decisões. A lista de pendências é o roteiro para fechar essa lacuna.
