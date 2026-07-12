// Carta
const regalo = document.querySelector(".regalo");
const regalos = document.querySelector(".regalos");
const modalCarta = document.getElementById("modalCarta");

regalo.addEventListener("click", () => {
  modalCarta.classList.add("activo");
});

regalos.addEventListener("click", () => {
  modalCarta.classList.add("activo");
});

modalCarta.addEventListener("click", () => {
  modalCarta.classList.remove("activo");
});

// Todo Oscuro + Soplido + Canción
const overlay = document.querySelector(".overlay");
const soplido = document.getElementById("soplido");
const cancion = document.getElementById("cancion");
const llamas = document.querySelectorAll(".llama");
const velasContainer = document.querySelector(".velas");

const celebrar = () => {
  soplido.currentTime = 0;
  soplido.play();

  llamas.forEach((l) => {
    l.style.animation = "apagar 0.5s forwards";
  });

  setTimeout(() => {
    velasContainer.classList.add("visible");
    cancion.currentTime = 0;
    cancion.play();
    overlay.classList.add("hidden");
  }, 1000);
};

llamas.forEach((l) => l.addEventListener("click", celebrar));
