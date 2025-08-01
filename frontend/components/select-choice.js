import Choices from 'choices.js';
import 'choices.js/public/assets/styles/choices.min.css';

export function initChoicesAjax(selector, url, options = {}) {
  const element = document.querySelector(selector);
  if (!element) return;

  // Zera valor anterior do <select>
  element.innerHTML = '<option value="">Selecione...</option>';

  const defaultConfig = {
    removeItemButton: true,
    searchEnabled: true,
    placeholderValue: 'Selecione...',
    noChoicesText: 'Nenhuma opção encontrada',
    shouldSort: false,
    ...options,
  };

  const choices = new Choices(element, defaultConfig);

  // Limpa as escolhas antes de carregar
  choices.clearStore();
  choices.clearChoices();
  choices.removeActiveItems();

  fetch(url)
    .then(res => res.json())
    .then(data => {
      const choicesData = data.map(item => ({
        value: item.id,
        label: item.text,
        selected: false, // importante!
      }));

      // 4º parâmetro = false para evitar manter seleção anterior
      choices.setChoices(choicesData, 'value', 'label', false);
    })
    .catch(err => console.error('Erro carregando dados para Choices:', err));

  return choices;
}
