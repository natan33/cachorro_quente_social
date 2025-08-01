import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  optimizeDeps: {
    include: ['jquery', 'bootstrap']  // Certifique-se de incluir o Bootstrap aqui para otimização
  },
  root: 'frontend',
  base: '/static/',
  build: {
    outDir: path.resolve(__dirname, 'app', 'static', 'dist'),
    assetsDir: '',
    manifest: true,  // Garante que o manifest seja gerado
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'frontend', 'main.js'),
        dashboard: path.resolve(__dirname, 'frontend', 'pages', 'dashboard.js'),
        registro_venda: path.resolve(__dirname, 'frontend', 'pages', 'registro_venda.js'),
        style: path.resolve(__dirname, 'frontend', 'main.css'),
      },
      // Não precisa usar 'external' aqui, porque o jQuery e Bootstrap serão importados
    },
  },
});
