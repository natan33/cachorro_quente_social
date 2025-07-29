// vite.config.js
import { defineConfig } from 'vite';
import path from 'path'; // Importe o módulo 'path'

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
        dashboard: 'frontend/dashboard.js',
        registro_venda: 'frontend/registro_venda.js',
        style: 'frontend/main.css',
      },
    },
  },
});