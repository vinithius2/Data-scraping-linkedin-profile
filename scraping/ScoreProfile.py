import json
from difflib import SequenceMatcher
from database.dao.PersonDao import PersonDao
from database.dao.SearchDao import SearchDao
from utils.bcolors import bcolors
from utils.texts import text_option_score, text_error_score


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
        self.MAX_PERCENT = 80
        self.database = database
        self.TECHNOLOGIES = "technologies"
        self.LANGUAGE = "language"
        self.LEVEL = "level"
        self.EDUCATION = "education"
        self.MESTRADO = "mestrado"
        self.DOUTORADO = "doutorado"
        self.POS_GRADUACAO = "pós graduação"
        self.POS = "pós"
        self.ESPECIALIZACAO = "especialização"
        self.GRADUACAO = "graduação"
        self.BACHAREL = "bacharel"
        self.TECNOLOGO = "tecnólogo"
        self.LEVEL_EDUCATION = "level_education"
        self.SR = "sênior"
        self.PL = "pleno"
        self.JR = "júnior"
        self.DEBUG = True
        self.job_characteristics = {
            "technologies": [],
            "language": ["inglês"],
            "level": ["sênior", "pleno", "júnior"]
        }

    def start(self):
        try:
            option = input(text_option_score)
            self.job_characteristics["technologies"] = [opt.strip() for opt in option.split(",")]
            list_result, search_list = self.__list_person()
            result_list = self.__weighted_calculation(list_result, search_list)
            if self.DEBUG:
                self.print_result(result_list)
            self.export(result_list)
            print(f"\n{bcolors.GREEN}Weighted calculation performed!{bcolors.ENDC}")
        except ValueError as e:
            print(text_error_score)
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
        for item in result:
            media = item["scores"]["media"]
            color, msg = self.get_color_media(media)
            media_text = f'{bcolors.BOLD}{color}{item["scores"]["media"]}{bcolors.ENDC}{bcolors.ENDC}'
            print(f'({item["search"].person_id}) [{media_text}] {bcolors.UNDERLINE}{bcolors.BOLD}{msg}{bcolors.ENDC}{bcolors.ENDC} - {item["search"].url_profile}')
            print(json.dumps(item["scores"], indent=4, ensure_ascii=False))
            print("\n")

    def get_color_media(self, media):
        color = None
        msg = None
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
        return color, msg

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
        |Tecnologias * |	0 a 1 ano	    |    3   |
        |              |    1 a 2 anos	    |    5   |
        |              |    2 a 3 anos	    |    7   |
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
        Tecnologias: Python, React, Node.js, TypeScript, React Native,
        ##########################################################################
        """
        result_list = list()
        for result in zip(list_result, search_list):
            result_dict = dict()
            person = result[0]
            search = result[1]
            score_dict = self.__create_dict_score()
            score_dict = self.__calculation_technologies(person, score_dict)
            score_dict = self.__calculation_language(person, score_dict)
            score_dict = self.__calculation_education(person, score_dict)
            score_dict = self.__calculation_level(person, score_dict)
            result_dict["person"] = person
            result_dict["search"] = search
            result_dict['scores'] = score_dict
            result_dict['scores']["media"] = self.__media(score_dict)
            result_list.append(result_dict)
        return result_list

    def __calculation_technologies(self, person, score_dict):
        score_dict = self.__set_time_experiences_descricao(person, score_dict, self.TECHNOLOGIES)
        score_dict, max_score_01 = self.__set_score_skills(person, score_dict, self.TECHNOLOGIES)
        score_dict, max_score_02 = self.__set_score_subtitle(person, score_dict, self.TECHNOLOGIES)
        score_dict, max_score_03 = self.__set_score_about(person, score_dict, self.TECHNOLOGIES)
        score_dict, max_score_04 = self.__set_score_certifications(person, score_dict, self.TECHNOLOGIES)
        score_dict[self.TECHNOLOGIES], max_score_05 = self.__set_score_experiences(score_dict[self.TECHNOLOGIES])
        self.max_score_technologies = sum([max_score_01, max_score_02, max_score_03, max_score_04, max_score_05])
        return score_dict

    def __calculation_language(self, person, score_dict):
        score_dict, max_score_06 = self.__set_score_languages(person, score_dict, self.LANGUAGE)
        score_dict, max_score_07 = self.__set_score_subtitle(person, score_dict, self.LANGUAGE)
        score_dict, max_score_08 = self.__set_score_about(person, score_dict, self.LANGUAGE)
        score_dict, max_score_09 = self.__set_score_skills(person, score_dict, self.LANGUAGE)
        score_dict, max_score_10 = self.__set_score_certifications(person, score_dict, self.LANGUAGE)
        self.max_score_language = sum([max_score_06, max_score_07, max_score_08, max_score_09, max_score_10])
        return score_dict

    def __calculation_education(self, person, score_dict):
        score_dict, max_score_11 = self.__set_score_education(person, score_dict)
        self.max_score_education = sum([max_score_11])
        return score_dict

    def __calculation_level(self, person, score_dict):
        score_dict, max_score_12 = self.set_score_experiences_cargo(person, score_dict)
        self.max_score_level = sum([max_score_12])
        return score_dict

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
        max_score = 0
        for key, value in score_dict.items():
            for k, v in value.items():
                max_score += v["score"]
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
        score_dict["education"] = dict()
        score_dict["education"][self.LEVEL_EDUCATION] = {"score": 0}
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
                if self.SR in experience.cargo.lower() or experience.descricao and self.SR in experience.descricao.lower():
                    if score_dict[self.LEVEL][self.SR]["score"] == 0:
                        score_dict[self.LEVEL][self.SR]["score"] += max_score
                        break
                elif self.PL in experience.cargo.lower() or experience.descricao and self.PL in experience.descricao.lower():
                    if score_dict[self.LEVEL][self.SR]["score"] == 0:
                        score_dict[self.LEVEL][self.PL]["score"] += 7
                        break
                elif self.JR in experience.cargo.lower() or experience.descricao and self.JR in experience.descricao.lower():
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
                    break
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
                        break
                    else:
                        if skill.indications < 20:
                            score_dict[main_key][key]['score'] += 2
                            break
                        elif 20 < skill.indications < 40:
                            score_dict[main_key][key]['score'] += 4
                            break
                        elif 40 < skill.indications < 60:
                            score_dict[main_key][key]['score'] += 6
                            break
                        elif 60 < skill.indications < 80:
                            score_dict[main_key][key]['score'] += 8
                            break
                        elif 80 < skill.indications < 99:
                            score_dict[main_key][key]['score'] += max_score
                            break
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
            if education.level:
                result = {
                    self.MESTRADO: self.similarity(education.level.lower(), self.MESTRADO),
                    self.DOUTORADO: self.similarity(education.level.lower(), self.DOUTORADO),
                    self.POS_GRADUACAO: max(self.similarity(education.level.lower(), self.POS_GRADUACAO), self.similarity(education.level.lower(), self.POS), self.similarity(education.level.lower(), self.ESPECIALIZACAO)),
                    self.GRADUACAO: max(self.similarity(education.level.lower(), self.GRADUACAO), self.similarity(education.level.lower(), self.BACHAREL)),
                    self.TECNOLOGO: self.similarity(education.level.lower(), self.TECNOLOGO)
                }
                key_max_value = max(result, key=result.get)
                all_values = result.values()
                max_value = max(all_values)

                if key_max_value == self.MESTRADO and max_value >= self.MAX_PERCENT:
                    score_dict[self.EDUCATION][self.LEVEL_EDUCATION]['score'] += max_score
                    break
                elif key_max_value == self.DOUTORADO and max_value >= self.MAX_PERCENT:
                    score_dict[self.EDUCATION][self.LEVEL_EDUCATION]['score'] += max_score
                    break
                elif key_max_value == self.POS_GRADUACAO and max_value >= self.MAX_PERCENT:
                    score_dict[self.EDUCATION][self.LEVEL_EDUCATION]['score'] += 8
                    break
                elif key_max_value == self.GRADUACAO and max_value >= self.MAX_PERCENT:
                    score_dict[self.EDUCATION][self.LEVEL_EDUCATION]['score'] += 7
                    break
                elif key_max_value == self.TECNOLOGO and max_value >= self.MAX_PERCENT:
                    score_dict[self.EDUCATION][self.LEVEL_EDUCATION]['score'] += 5
                    break
        return score_dict, max_score

    def similarity(self, text_db, text_static):
        seq = SequenceMatcher(None, text_db, text_static)
        percent = seq.ratio() * 100
        return round(percent, 2)

