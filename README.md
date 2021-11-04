# Sobre
Essa aplicação tem como objetivo gerar um relatório inteligente sobre possíveis candidatos a vagas de emprego baseando-se em um filtro de tecnologias e por um cálculo ponderado para cada campo do perfil do Linkedin.

![menu](https://user-images.githubusercontent.com/7644485/140386425-a5350a1e-4b86-47a5-9300-7e0665f67883.png)

## Primeira etapa
Adicionar um filtro de pessoas na entrada da aplicação e salvar essa lista filtrada para ser realizado o Scraping posteriormente, exemplo de URL aceita: https://www.linkedin.com/search/results/people/?keywords=desenvolvedor&origin=CLUSTER_EXPANSION&sid=FR%3B

![search](https://user-images.githubusercontent.com/7644485/140386464-b6ad2422-1c88-4620-8a02-12e8575b104b.png)

## Segunda etapa
Iniciar o scraping de cada perfil pesquisado na primeira etapa e obter todas as informações possíveis e salvar no banco de dados.

## Terceira etapa
Selecionar a lista pesquisada e adicionar as tecnologias para realizar o cálculo ponderado e obter a média daquele perfil baseando-se nos dados de entrada e por alguns fatores como o idioma Inglês, nível profissional, tempo de experiência das tecnologias e etc. Segue tabela de cálculo.

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
É o total de pontos que o algoritimo obteve do perfil.
### máximo_de_pontos_por_filtro 
É o total máximo de pontos permitido baseando-se no cálculo com o filtro, esse total pode variar de acordo com a quantidade de filtros usados.
### Média Ponderada
_(pontos_por_perfil/máximo_de_pontos_por_filtro) * 100 = media_	

Após o cálculo ponderado é realizado a exportação para um arquivo XLS com os dados detalhados e de forma organizada e amigavel ao usuário. Dessa maneira, o profissional de RH poderá agilizar suas tomadas de decisão com um algoritmo inteligente e rápido.

## Pontos de observação

Atualmente essa versão se encontra em teste, o que torna plausível alguns comportamentos imprevisíveis, pois o _Data Scraping_ utiliza-se de classes, tags e ids do _HTML_ para obter os dados, se o _Linkedin_ mudar essas referências, o comportamento dessa aplicação pode ser inesperado. A quantidade de requisições utilizadas pelo algoritimo pode gerar algum alerta para a equipe de _Blue Team_ do _Linkedin_, o que pode ocorrer de derrubar a sua seção ou solicitar alguma alternativa de verificação para identificar se você é um "robô" ou não, caso ocorra algum comportamento estranho, não hesite de entrar em contato. Porém, não se preocupe, foi feito vários testes para reverter essa situação, caso ocorra, a automação pode parar e aguardar ação humana para prosseguir.

Outro ponto relevante é que essa aplicação não salva os dados de login e senha do usuário, isso é feito de forma manual no navegador quando a aplicação se encontra em modo de não _debug_, caso o _debug_ esteja habilitado, utiliza-se os valores já salvo nas variáveis de ambiente do SO, isso só é útil para desenvovledores, fique tranquilo, seu _Linkedin_ está a salvo, o código é aberto, veja por você mesmo.
