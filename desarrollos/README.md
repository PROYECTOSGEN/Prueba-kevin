# desarrollos/

**Todo lo que se EJECUTA:** un HTML, un script, una automatización, una
aplicación que se compila.

```
desarrollos/
└── <nombre>/
    ├── app/              ← el código, siempre aquí
    ├── README.md         ← qué hace y cómo se corre
    └── desarrollo.json   ← la ficha
```

La ficha `desarrollo.json` lleva: `nombre`, `estado`, `tipo`, `area`, `que_hace`
y `despliegue`. Sin ficha, el guardián marca el push en rojo.

**No se crean repositorios sueltos para esto.** Un desarrollo vive dentro de su
proyecto. Solo uno del tamaño de ESPARQ nace en una organización propia, y eso
se pregunta antes.

**Detente y pregunta antes de escribir** si el desarrollo necesita llaves de
servidor o va a guardar datos personales: todo el equipo con acceso a este
repositorio lo va a ver.

**Las llaves nunca se suben.** Ni `.env`, ni `.pem`, ni JSON de credenciales. El
guardián los caza, pero para entonces ya están en el historial y sacarlos exige
reescribirlo **y rotar** las llaves.
