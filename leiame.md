# Programa para extração de informações de formulários para tabulação

O programa IMG2CSV é um wrapper Tesseract-OCR para transformar capturas de tela de formulários em tabelas CSV. O programa realiza a deleção do cabeçalho/resposta através dos dois pontos no final de cada etiqueta, por exemplo:

```html
<form>
<label>Nome de usuário:</label>
<input value="algum texto">
</form>
```

Este HTML irá gerar um formulário simples com uma etiqueta `Nome de usuário:` ​​​​e um campo para o valor, que pode ser qualquer informação. Com base nos critérios previamente estabelecidos, `Nome de usuário:` ​​​​será o cabeçalho da tabela e o valor de entrada `algum texto` será o seu valor.

Este programa depende da instalação do Tesseract-OCR e do pacote de idioma português, que pode ser baixado nos links abaixo:

* Tesseract para Windows: <https://github.com/UB-Mannheim/tesseract/releases/latest>

* Modelo treinado em português: <https://github.com/tesseract-ocr/tessdata_best/blob/main/por.traineddata>

O ícone deste programa foi criado com imagens do banco de imagens Pixabay:

* Ícone de imagem: [https://pixabay.com/pt/users/raphaelsilva-4702998/](https://pixabay.com/pt/users/raphaelsilva-4702998/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=2160911) por Raphael Silva.

* Ícone de tabela: [https://pixabay.com/pt/users/inspire-studio-22128832/](https://pixabay.com/pt/users/inspire-studio-22128832/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7040220) por inspire-studio.
