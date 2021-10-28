import json

from database.dao.PersonDao import PersonDao
from database.dao.SearchDao import SearchDao
from utils.bcolors import bcolors


class ScoreProfile:
    def __init__(self, database):
        self.zero_ano = 0
        self.um_ano = 12
        self.dois_anos = 24
        self.tres_anos = 36
        self.max_score_technologies = 0
        self.max_score_language = 0
        self.max_score_education = 0
        self.max_score_level = 0
        self.database = database
        self.TECHNOLOGIES = "technologies"
        self.LANGUAGE = "language"
        self.LEVEL = "level"
        self.EDUCATION = "education"
        self.SR = "sênior"
        self.PL = "pleno"
        self.JR = "júnior"
        self.text_error = f"""\n
            {bcolors.FAIL}
            {bcolors.HEADER}######## ATTEMTION ########{bcolors.ENDC}
            {bcolors.UNDERLINE}Error, repeat the procedure!{bcolors.ENDC}
            {bcolors.HEADER}###########################{bcolors.ENDC}\n
            {bcolors.ENDC}
            """
        self.text_option = f"""
            {bcolors.HEADER}########## Add comma-separated technologies to punctuation ##########{bcolors.ENDC}\n
            {bcolors.UNDERLINE}Example:{bcolors.ENDC} python, react, node, typescript, react native\n\n
            {bcolors.HEADER}###########################{bcolors.ENDC}\n
            {bcolors.BOLD}{bcolors.CYAN}* Add your technologies: {bcolors.ENDC}{bcolors.ENDC}
            """
        self.job_characteristics = {
            "technologies": [],
            "language": {"inglês": ["avançado", "fluente"]},
            "level": ["sênior", "pleno", "júnior"]
        }

    def start(self):
        try:
            option = input(self.text_option)
            self.job_characteristics["technologies"] = [opt.strip() for opt in option.split(",")]
            list_result, search_list = self.__list_person()
            result_list = self.__weighted_calculation(list_result, search_list)
            self.print_result(result_list)
            self.export(result_list)
            print(f"\n{bcolors.GREEN}Weighted calculation performed!{bcolors.ENDC}")
        except ValueError as e:
            print(self.text_error)
            self.start()

    def __list_person(self):
        search_list = SearchDao(self.database).select_search_person_id_is_not_null()
        list_result = list()
        for search in search_list:
            list_result.append(PersonDao(database=self.database).select_people_by_id(search.person_id))
        return list_result, search_list

    def export(self, result_list):
        pass

    def print_result(self, result_list):
        print(f"{bcolors.HEADER}### DICT FILTER ####{bcolors.ENDC}\n")
        print(json.dumps(self.job_characteristics, indent=4, ensure_ascii=False))
        print(f"{bcolors.HEADER}### RESULT SCORES ####{bcolors.ENDC}\n")
        result = sorted(result_list, key=lambda d: d['scores']['media'], reverse=True)
        color = None
        msg = None
        for item in result:
            media = item["scores"]["media"]
            if media < 25:
                color = bcolors.RED
                msg = "It's not good..."
            elif 25 < media < 50:
                color = bcolors.ORANGE
                msg = "Ok..."
            elif 50 < media < 75:
                color = bcolors.YELLOW
                msg = "Good!"
            elif media > 75:
                color = bcolors.GREEN
                msg = "Great!!!"
            # print(f"{bcolors.HEADER}###########################{bcolors.ENDC}")
            # print(f"{bcolors.BOLD}Pontos máximo de cada chave:{bcolors.ENDC} {max_score}")
            # print(f"{bcolors.BOLD}Todos os pontos por perfil:{bcolors.ENDC} {sum_scores}")
            # print(f"{bcolors.BOLD}Média calculada:{bcolors.ENDC} {round(percent_media, 2)}")
            # print(f"{bcolors.HEADER}###########################{bcolors.ENDC}")
            media_text = f'{bcolors.BOLD}{color}{item["scores"]["media"]}{bcolors.ENDC}{bcolors.ENDC}'
            print(f'[{media_text}] {bcolors.UNDERLINE}{bcolors.BOLD}{msg}{bcolors.ENDC}{bcolors.ENDC} - {item["search"].url_profile}')
            print(json.dumps(item["scores"], indent=4, ensure_ascii=False))
            print("\n")

    def __calculate_time(self, anos, meses):
        anos = anos or 0
        meses = meses or 0
        result = (anos * 12) + meses
        return result

    def __weighted_calculation(self, list_result, search_list):
        """
        ############# Cálculo Ponderado ##############
        |--------------------------------------------|
        |Caracteristicas		  |              Peso|
        |--------------------------------------------|
        |Subtitulo *		                  |  2   |
        |--------------------------------------------|
        |Sobre *		                      |  5   |
        |--------------------------------------------|
        |Sênior		              |              10  |
        |--------------------------------------------|
        |Pleno		              |              7   |
        |--------------------------------------------|
        |Júnior		              |              3   |
        |--------------------------------------------|
        |Inglês	   |    Fluente ou Nativo  |     10  |
        |          |    Avançado	       |     10  |
        |          |    Intermediário	   |     7   |
        |          |    Básico a intermediário | 4   |
        |          |    Básico             |     1   |
        |--------------------------------------------|
        |Tecnologias * |	0 a 1 ano	    |    4   |
        |              |    1 a 2 anos	    |    6   |
        |              |    2 a 3 anos	    |    8   |
        |              |    3 anos +	    |    10  |
        |--------------------------------------------|
        |Skills *	 |    0 a 20 indicações	  |  2   |
        |            |    20 a 40 indicações  |  4   |
        |            |    40 a 60 indicações  |  6   |
        |            |    60 a 80 indicações  |  8   |
        |            |    80 a 99 indicações  |  10  |
        |--------------------------------------------|
        |Certificações *		              |  5   |
        |--------------------------------------------|
        |Mestrado		          |              10  |
        |Doutorado		          |              10  |
        |Pós graduação		      |              8   |
        |Graduação		          |              7   |
        |Técnologo      		  |              5   |
        |--------------------------------------------|

        * Ex:
        ##########################################################################
        Tecnologias principais: Python, React, Node.js, TypeScript, React Native,
        Requisitos: Perfis pleno e sênior, inglês avançado/fluente
        ##########################################################################
        * Max score:
        By tem technology: 36
        By item language: 36
        By item level experience: 10
        ##########################################################################
        """
        result_list = list()
        for result in zip(list_result, search_list):
            result_dict = dict()
            person = result[0]
            search = result[1]
            score_dict = self.__create_dict_score()
            # TECHNOLOGIES
            score_dict = self.__set_time_experiences_descricao(person, score_dict, self.TECHNOLOGIES)
            score_dict, max_score_01 = self.__set_score_skills(person, score_dict, self.TECHNOLOGIES)
            score_dict, max_score_02 = self.__set_score_subtitle(person, score_dict, self.TECHNOLOGIES)
            score_dict, max_score_03 = self.__set_score_about(person, score_dict, self.TECHNOLOGIES)
            score_dict, max_score_04 = self.__set_score_certifications(person, score_dict, self.TECHNOLOGIES)
            score_dict[self.TECHNOLOGIES], max_score_05 = self.__set_score_experiences(score_dict[self.TECHNOLOGIES])
            self.max_score_technologies = sum([max_score_01, max_score_02, max_score_03, max_score_04, max_score_05])
            # LANGUAGE
            score_dict, max_score_06 = self.__set_score_languages(person, score_dict, self.LANGUAGE)
            score_dict, max_score_07 = self.__set_score_subtitle(person, score_dict, self.LANGUAGE)
            score_dict, max_score_08 = self.__set_score_about(person, score_dict, self.LANGUAGE)
            score_dict, max_score_09 = self.__set_score_skills(person, score_dict, self.LANGUAGE)
            score_dict, max_score_10 = self.__set_score_certifications(person, score_dict, self.LANGUAGE)
            self.max_score_language = sum([max_score_01, max_score_02, max_score_03, max_score_04, max_score_05])
            # EDUCATION
            score_dict, max_score_11 = self.__set_score_education(person, score_dict)
            self.max_score_education = sum([max_score_11])
            # LEVEL
            score_dict, max_score_12 = self.set_score_experiences_cargo(person, score_dict)
            self.max_score_level = sum([max_score_12])
            # FINISH
            result_dict["person"] = person
            result_dict["search"] = search
            result_dict['scores'] = score_dict
            result_dict['scores']["media"] = self.__media(score_dict)
            result_list.append(result_dict)
        return result_list

    def __media(self, score_dict):
        """
        Calculo da média ponderada
        """
        max_score = self.__max_score(score_dict)
        sum_scores = self.__sum_all_scores(score_dict)
        media = (sum_scores / max_score) * 100
        return round(media, 2)

    def __sum_all_scores(self, score_dict):
        """
        Soma todos os pontos por perfil
        """
        for key, value in score_dict.items():
            max_score = 0
            for key, value in value.items():
                max_score += value["score"]
            return max_score

    def __max_score(self, score_dict):
        """
        Soma todos os pontos máximo de cada chave
        """
        result_media_score = 0
        for key, value in score_dict.items():
            if key == self.TECHNOLOGIES:
                result_media_score += len(value) * self.max_score_technologies
            elif key == self.LANGUAGE:
                result_media_score += len(value) * self.max_score_language
            elif key == self.LEVEL:
                result_media_score += len(value) * self.max_score_level
            elif key == self.EDUCATION:
                result_media_score += len(value) * self.max_score_level
        return result_media_score

    def __create_dict_score(self):
        """
        Cria um dicionario para administrar as pontuações de cada perfil.
        """
        score_dict = dict()
        score_dict["technologies"] = dict()
        for technologie in list(set(self.job_characteristics["technologies"])):
            score_dict["technologies"][technologie] = {"tempo": 0, "score": 0}
        score_dict["language"] = dict()
        for language in list(set(self.job_characteristics["language"])):
            score_dict["language"][language] = {"score": 0}
        score_dict["level"] = dict()
        for level in list(set(self.job_characteristics["level"])):
            score_dict["level"][level] = {"score": 0}
        score_dict["education"] = {"score": 0}
        return score_dict

    def __set_score_subtitle(self, person, score_dict, main_key):
        """
        Adiciona a pontuação do subtitulo baseado nas palavras chaves.
        """
        max_score = 2
        for key, score in score_dict[main_key].items():
            if key in person.subtitle.lower():
                score_dict[main_key][key]['score'] += max_score
        return score_dict, max_score

    def __set_score_about(self, person, score_dict, main_key):
        """
        Adiciona a pontuação ao sobre baseado nas palavras chaves.
        """
        max_score = 5
        for key, score in score_dict[main_key].items():
            if person.about and key in person.about.lower():
                score_dict[main_key][key]['score'] += max_score
        return score_dict, max_score

    def __set_time_experiences_descricao(self, person, score_dict, main_key):
        """
        Faz a soma do tempo percorrendo as experiências para cada tecnologia.
        """
        for key, score in score_dict[main_key].items():
            for experience_list in person.experiences:
                for experience in experience_list:
                    if key in experience.cargo.lower() or experience.descricao and key in experience.descricao.lower():
                        tempo = self.__calculate_time(experience.anos, experience.meses)
                        score_dict[main_key][key]['tempo'] += tempo
        return score_dict

    def set_score_experiences_cargo(self, person, score_dict):
        """
        Verifica se existe no 'saco de palavras' as palavras 'sênior', 'pleno' e 'júnior', caso exista algum, o loop é
        interrompido, pois só é válido uma única validação buscando a experiência mais recente até a mais antiga.
        """
        max_score = 10
        for experience_list in person.experiences:
            for experience in experience_list:
                if self.SR in experience.cargo or experience.descricao and self.SR in experience.descricao:
                    if score_dict[self.LEVEL][self.SR]["score"] == 0:
                        score_dict[self.LEVEL][self.SR]["score"] += max_score
                        break
                elif self.PL in experience.cargo or experience.descricao and self.PL in experience.descricao:
                    if score_dict[self.LEVEL][self.SR]["score"] == 0:
                        score_dict[self.LEVEL][self.PL]["score"] += 7
                        break
                elif self.JR in experience.cargo or experience.descricao and self.JR in experience.descricao:
                    if score_dict[self.LEVEL][self.SR]["score"] == 0:
                        score_dict[self.LEVEL][self.JR]["score"] += 3
                        break
        return score_dict, max_score

    def __set_score_experiences(self, technologies):
        """
        Adiciona os pontos de cada tecnologia baseado no tempo de experiência.
        """
        max_score = 10
        for key, value in technologies.items():
            tempo = value["tempo"]
            if self.zero_ano > tempo < self.um_ano:
                technologies[key]['score'] += 3
            elif self.um_ano < tempo < self.dois_anos:
                technologies[key]['score'] += 5
            elif self.dois_anos < tempo < self.tres_anos:
                technologies[key]['score'] += 7
            elif tempo > self.tres_anos:
                technologies[key]['score'] += max_score
        return technologies, max_score

    def __set_score_certifications(self, person, score_dict, main_key):
        """
        Adiciona a pontuação dos certificados.
        """
        max_score = 5
        for key, score in score_dict[main_key].items():
            for certification in person.certifications:
                if key in certification.titulo.lower():
                    score_dict[main_key][key]['score'] += max_score
        return score_dict, max_score

    def __set_score_skills(self, person, score_dict, main_key):
        """
        Adiciona a pontuação da skill baseado nas indicações.
        """
        max_score = 10
        for key, score in score_dict[main_key].items():
            for skill in person.skills:
                if key in skill.titulo.lower():
                    if skill.verify:
                        score_dict[main_key][key]['score'] += max_score
                    else:
                        if skill.indications < 20:
                            score_dict[main_key][key]['score'] += 2
                        elif 20 < skill.indications < 40:
                            score_dict[main_key][key]['score'] += 4
                        elif 40 < skill.indications < 60:
                            score_dict[main_key][key]['score'] += 6
                        elif 60 < skill.indications < 80:
                            score_dict[main_key][key]['score'] += 8
                        elif 80 < skill.indications < 99:
                            score_dict[main_key][key]['score'] += max_score
        return score_dict, max_score

    def __set_score_languages(self, person, score_dict, main_key):
        """
        Adiciona a pontuação do idioma baseado no nível.
        """
        max_score = 10
        for key, score in score_dict[main_key].items():
            for language in person.languages:
                if key in language.idioma.lower():
                    if language.nivel:
                        level = language.nivel.lower().replace("nível", "").strip()
                        if level == "fluente ou nativo":
                            score_dict[main_key][key]['score'] += max_score
                        elif level == "avançado":
                            score_dict[main_key][key]['score'] += max_score
                        elif level == "intermediário":
                            score_dict[main_key][key]['score'] += 7
                        elif level == "básico a intermediário":
                            score_dict[main_key][key]['score'] += 4
                        elif level == "básico":
                            score_dict[main_key][key]['score'] += 1
        return score_dict, max_score

    def __set_score_education(self, person, score_dict):
        """
        Adiciona a pontuação baseado na educação.
        """
        max_score = 10
        for education in person.education:
            if education.level == "mestrado":
                score_dict[self.EDUCATION]['score'] += max_score
                break
            elif education.level == "doutorado":
                score_dict[self.EDUCATION]['score'] += max_score
                break
            elif education.level == "pós graduação" or education.level == "pós":
                score_dict[self.EDUCATION]['score'] += 8
                break
            elif education.level == "graduação" or education.level == "bacharel":
                score_dict[self.EDUCATION]['score'] += 7
                break
            elif education.level == "técnologo":
                score_dict[self.EDUCATION]['score'] += 5
                break
        return score_dict, max_score
