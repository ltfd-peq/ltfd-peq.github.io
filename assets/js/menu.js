// Menu móvel acessível (PLANO §8.6, C4).
// Sem JS, o link "Menu" leva ao mapa do site no rodapé; com JS, vira um
// <button aria-expanded> que abre o painel. Esc fecha e devolve o foco ao botão;
// enquanto o painel está aberto, o resto da página fica inert (foco não se perde atrás dele).
(() => {
  const nav = document.querySelector("[data-nav]");
  if (!nav) return;
  const botao = nav.querySelector(".nav__botao");
  const semJs = nav.querySelector(".nav__sem-js");
  const rotulo = botao.querySelector(".nav__botao-rotulo");
  const fora = document.querySelectorAll("main, footer, .pular");
  const desktop = window.matchMedia("(min-width: 64em)");

  botao.hidden = false;
  semJs.hidden = true;

  const aberto = () => nav.hasAttribute("data-aberto");

  function definir(abrir, devolverFoco) {
    botao.setAttribute("aria-expanded", String(abrir));
    rotulo.textContent = abrir ? botao.dataset.rotuloFechar : botao.dataset.rotuloAbrir;
    nav.toggleAttribute("data-aberto", abrir);
    document.documentElement.classList.toggle("menu-aberto", abrir);
    fora.forEach((el) => { el.inert = abrir; });
    if (!abrir && devolverFoco) botao.focus();
  }

  botao.addEventListener("click", () => definir(!aberto(), false));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && aberto()) definir(false, true);
  });
  nav.querySelectorAll(".nav__painel a").forEach((a) => {
    a.addEventListener("click", () => definir(false, false));
  });
  desktop.addEventListener("change", (e) => { if (e.matches && aberto()) definir(false, false); });
})();
