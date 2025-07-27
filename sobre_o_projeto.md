# Como configurar o front-end com Node.js e Vite

## Passo 1: Inicialize o projeto Node.js

```bash
npm init -y
```

## Passo 2: Instale as dependências necessárias

```bash
# Dependências para o front-end
npm install bootstrap jquery datatables.net --save

# Vite e plugins
npm install vite @vitejs/plugin-vue @vitejs/plugin-react

# Se for trabalhar com SASS
npm install sass
```

## Passo 3: Crie o arquivo `vite.config.js`

Exemplo:

```js
// vite.config.js
import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  // ...
  root: 'frontend', // Onde seu código fonte do front-end está
  base: '/static/', // URL base para os assets no Flask (Flask serve de /static/)
  build: {
    // Use path.resolve para um caminho absoluto e explícito
    outDir: path.resolve(__dirname, 'app', 'static', 'dist'), // <-- ATENÇÃO AQUI!
    assetsDir: '',
    manifest: true,
    // manifestFilename: 'manifest.json', // Geralmente não é necessário, mas pode tentar se nada mais funcionar
    rollupOptions: {
      input: {
        main: 'frontend/main.js',
        style: 'frontend/main.css',
      },
    },
  },
});
```

## Passo 5: Crie um diretório `frontend` na raiz do seu projeto

Sugestão de estrutura:

```
frontend/
├── main.js         # Arquivo principal JS
├── main.css        # Arquivo principal CSS
├── components/     # Componentes JS ou Vue/React
├── assets/         # Imagens, fontes, etc
├── pages/          # Páginas do front-end (opcional)
```

Adapte conforme sua stack (Vue, React, JS puro, etc).

## Passo 6: Instale todas as dependências do projeto

```bash
npm install
```

---

**Observações:**
- Certifique-se de que o diretório `frontend` existe e contém seus arquivos JS/CSS principais.
- O Vite irá gerar os arquivos em `app/static/dist` para serem servidos pelo Flask.
- Ajuste os caminhos conforme a estrutura do seu projeto.


# Instale todas as dependências do projeto
npm install

