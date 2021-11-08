_Download V1.0:_ https://github.com/vinithius2/scraping-data-linkedin-profile/raw/main/dist/Linkedin_Scraping_Profile_v1.0.zip

# Sobre (About)
_**PT:**_ Essa aplicação tem como objetivo gerar um relatório inteligente sobre possíveis candidatos a vagas de emprego baseando-se em um filtro de tecnologias e por um cálculo ponderado para cada campo do perfil do Linkedin.

_**ENG:**_ This application aims to generate an intelligent report on possible job applicants based on a technology filter and a weighted calculation for each field in the LinkedIn profile.

![search](https://user-images.githubusercontent.com/7644485/140811897-90b15082-78a8-422d-b1df-7261174bfe51.png)

![menu](https://user-images.githubusercontent.com/7644485/140386425-a5350a1e-4b86-47a5-9300-7e0665f67883.png)

## Primeira etapa (First step)
_**PT:**_ Adicionar um filtro de pessoas na entrada da aplicação e salvar essa lista filtrada para ser realizado o Scraping posteriormente, exemplo de URL aceita: https://www.linkedin.com/search/results/people/?keywords=desenvolvedor&origin=CLUSTER_EXPANSION&sid=FR%3B

_**ENG:**_ Add a people filter in the application entry and save this filtered list to be Scraping later, example URL accepted: https://www.linkedin.com/search/results/people/?keywords=desenvolvedor&origin=CLUSTER_EXPANSION&sid=FR%3B

![search](https://user-images.githubusercontent.com/7644485/140386464-b6ad2422-1c88-4620-8a02-12e8575b104b.png)

## Segunda etapa (Second step)
_**PT:**_ Iniciar o scraping de cada perfil pesquisado na primeira etapa e obter todas as informações possíveis e salvar no banco de dados.

_**ENG:**_ Start scraping each profile searched in the first step and get as much information as possible and save it to the database.

## Terceira etapa (third step)
_**PT:**_ Selecionar a lista pesquisada e adicionar as tecnologias para realizar o cálculo ponderado e obter a média daquele perfil baseando-se nos dados de entrada e por alguns fatores como o idioma Inglês, nível profissional, tempo de experiência das tecnologias e etc. Segue tabela de cálculo.

_**ENG:**_ Select the searched list and add the technologies to perform the weighted calculation and obtain the average of that profile based on the input data and some factors such as the English language, professional level, time of experience with the technologies, etc. Calculation table follows.

Grupo | Caracteristicas   | Peso
:------: | :------: | :------:
Info|Subtitulo *	 | 2
Info|Sobre *	 | 5
Nível profissional|Sênior	 | 10
Nível profissional|Pleno	 | 7
Nível profissional|Júnior	 | 3
Inglês|Fluente ou nativo	 | 10
Inglês|Avançado	 | 8
Inglês|Intermediário	 | 6
Inglês|Básico a intermediário	 | 4
Inglês|Básico	 | 1
Tecnologias * |0 a 1 ano |	3
Tecnologias * |1 a 2 anos |	5
Tecnologias * |2 a 3 anos |	7
Tecnologias * |3 anos + |	10
Skills * | 0 a 20 indicações |	2
Skills * | 20 a 40 indicações |	4
Skills * | 40 a 60 indicações |	6
Skills * | 60 a 80 indicações |	8
Skills * | 80 a 99 indicações |	10
Skills * | Selo Linkedin | 10
Educação  | Certificações *  | 5
Educação  | Mestrado | 10
Educação  | Doutorado | 10
Educação  | Pós graduação | 8
Educação  | Graduação | 7
Educação  | Tecnólogo | 5

### pontos_por_perfil 

_**PT:**_ É o total de pontos que o algoritimo obteve do perfil.

_**ENG:**_ It is the total points that the algorithm got from the profile.

### máximo_de_pontos_por_filtro 

_**PT:**_ É o total máximo de pontos permitido baseando-se no cálculo com o filtro, esse total pode variar de acordo com a quantidade de filtros usados.

_**ENG:**_ It is the maximum total of points allowed based on the calculation with the filter, this total may vary according to the amount of filters used.

### Média Ponderada (Weighted Average)
_(pontos_por_perfil/máximo_de_pontos_por_filtro) * 100 = media_	

_**PT:**_ Após o cálculo ponderado é realizado a exportação para um arquivo XLS com os dados detalhados e de forma organizada e amigavel ao usuário. Dessa maneira, o profissional de RH poderá agilizar suas tomadas de decisão com um algoritmo inteligente e rápido.

_**ENG:**_ After the weighted calculation is carried out the export to an XLS file with detailed data in an organized and user-friendly way. In this way, the HR professional will be able to streamline their decision making with an intelligent and fast algorithm.

![xls](https://user-images.githubusercontent.com/7644485/140517186-c0a96cd9-2440-432c-8bcf-61fed5a6f7c2.png)

## Pontos de observação (observation points)

_**PT:**_ Atualmente essa versão se encontra em teste, o que torna plausível alguns comportamentos imprevisíveis, pois o _Data Scraping_ utiliza-se de classes, tags e ids do _HTML_ para obter os dados, se o _Linkedin_ mudar essas referências, o comportamento dessa aplicação pode ser inesperado. A quantidade de requisições utilizadas pelo algoritimo pode gerar algum alerta para a equipe de _Blue Team_ do _Linkedin_, o que pode ocorrer de derrubar a sua seção ou solicitar alguma alternativa de verificação para identificar se você é um "robô" ou não, caso ocorra algum comportamento estranho, não hesite de entrar em contato. Porém, não se preocupe, foi feito vários testes para reverter essa situação, caso ocorra, a automação pode parar e aguardar ação humana para prosseguir.

Outro ponto relevante é que essa aplicação não salva os dados de login e senha do usuário, isso é feito de forma manual no navegador quando a aplicação se encontra em modo de não _debug_, caso o _debug_ esteja habilitado, utiliza-se os valores já salvo nas variáveis de ambiente do SO, isso só é útil para desenvovledores, fique tranquilo, seu _Linkedin_ está a salvo, o código é aberto, veja por você mesmo.

_**ENG:**_ This version is currently under testing, which makes some unpredictable behavior plausible, as _Data Scraping_ uses _HTML_ classes, tags and ids to obtain the data, if _Linkedin_ changes these references, the behavior of this application may be unexpected . The number of requests used by the algorithm can generate an alert for the _Blue Team_ team of _Linkedin_, which can occur to bring down your section or request some alternative verification to identify if you are a "robot" or not, if any occurs strange behavior, please feel free to get in touch. However, don't worry, several tests were done to reverse this situation, if it happens, the automation can stop and wait for human action to proceed.

Another relevant point is that this application does not save the user's login and password data, this is done manually in the browser when the application is in non-debug_ mode, if _debug_ is enabled, the values already saved are used in the OS environment variables, this is only useful for developers, rest assured, your _Linkedin_ is safe, the source is open source, see for yourself.

## Criar .EXE (Create .EXE)

_**PT:**_ Use o terminal com a virtualenv ativada e com as bibliotecas instaladas e execute o seguinte script:

_**ENG:**_ Use the terminal with virtualenv enabled and the libraries installed and run the following script:

~~~python
pyinstaller --onefile --console --icon=favicon_likedin_scraping.ico --name=Linkedin_Scraping_Profile_v0.0 main.py
~~~

_**PT:**_ O executável se encontrará na pasta **dist/**

_**ENG:**_ The executable will be found in the folder **dist/**
