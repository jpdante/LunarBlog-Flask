# LunarBlog-Flask
Projeto de blog desenvolvido utilizando Python, Flask, SQLAlchemy, Bootstrap, jQuery e Font Awesome.

## Bibilotecas/Pacotes
O projeto necessita das seguintes bibliotecas / pacotes para iniciar:

`flask`, `flask_sqlalchemy`, `flask_migrate`, `argon2-cffi`, `pyjwt[crypto]`, `markdown`

Utilize o seguinte comando para instalar os pacotes em um novo environment:
```console
pip install virtualenv
python -m venv ./venv
pip install flask flask_sqlalchemy flask_migrate argon2-cffi pyjwt[crypto] markdown
```
## Uso
Para iniciar o projeto utilize o seguinte comando:

```console
./.venv/Scripts/Activate.ps1
python -m flask --app __init__.py run
```

Conta padrão:
```
Email: admin@admin.com
Senha: admin
```

## Projeto
Este projeto foi desenvolvido para o curso de Python avançado para web com flask.