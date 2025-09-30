# IMG2CSV

The IMG2CSV program is a Tesseract-OCR wrapper to transform form screenshots into CSV tables. The program performs header/response deletion through the colon at the end of each tag, for example:

```html
<form>
<label>Username:</label>
<input value="some text">
</form>
```

This HTML will generate a simple form with a `Username:` ​​tag and a field for the value, which can be any information. Based on the previously established criteria, `Username:` ​​will be the table header and the input value `some text` will be its value.

This program depends on the installation of Tesseract-OCR and the Portuguese language pack, which can be downloaded from the links below:

* Tesseract download for Windows: https://github.com/UB-Mannheim/tesseract/releases/latest

* Trained portuguese language data: https://github.com/tesseract-ocr/tessdata/raw/main/por.traineddata

The icon for this program was created with images from the Pixabay image bank:

* Image icon: [https://pixabay.com/pt/users/raphaelsilva-4702998/](https://pixabay.com/pt/users/raphaelsilva-4702998/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=2160911) by Raphael Silva.

* Sheet icon: [https://pixabay.com/pt/users/inspire-studio-22128832/](https://pixabay.com/pt/users/inspire-studio-22128832/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7040220) by inspire-studio.
