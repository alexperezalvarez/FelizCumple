# 🎂 Feliz Cumpleaños

Página web interactiva de cumpleaños sorpresa con confeti animado, torta con vela, caja de regalo y carta personalizada.

## ✨ Funcionalidades

- 🎊 **Confeti animado** en dos capas (fondo y frente)
- 🖼️ **Portarretrato** con video
- 🎂 **Torta de cumpleaños** con vela y llama animada
  - Click en la llama → se apaga, suena un soplido y comienza la canción
- 🎁 **Caja de regalo** con animación "bouncing" y estrellas giratorias
  - Click en la caja → abre una carta modal con mensaje personalizado
- 🌑 **Overlay oscuro** inicial que se desvanece al apagar la vela
- 📱 **Diseño responsive** (mobile y desktop)

## 🚀 Deploy en Netlify

1. Conectá el repositorio a [Netlify](https://app.netlify.com/)
2. **Build command:** _(ninguno, es estático)_
3. **Publish directory:** `.`

O arrastrá la carpeta a [Netlify Drop](https://app.netlify.com/drop).

## 📁 Estructura

```
├── index.html
├── styles.css
├── mobile.css
├── Confeti.js
├── Confeti2.js
├── Sorpresa.js
├── recursos/
│   ├── Mar.mp4
│   ├── cancion.mp3
│   ├── soplar1.mp3
│   ├── soplar2.mp3
│   └── cumpleañero.png
└── README.md
```

## 🛠️ Tecnologías

HTML5, CSS3 (animaciones, flexbox, clip-path, keyframes), JavaScript (Canvas API)

Hecho con ❤️ por Alex
