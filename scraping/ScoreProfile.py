from operator import itemgetter
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
        self.database = database
        self.ignore_chars = [",", ".", "|", "/", "\\", "(", ")", "[", "]", "{", "}", "-", "_", " "]
        self.ignore_propositions = [
            'o', 'duns', 'do', 'aos', 'os', 'dos', 'por', 'pela', 'umas', 'à', 'de', 'das', 'a', 'e', 'uns', 'duma',
            'uma', 'numa', 'pelas', 'pelo', 'às', 'na', 'num', 'per', 'ao', 'pelos', 'as', 'no', 'dumas', 'em', 'nuns',
            'um', 'nas', 'dum', 'da', 'numas', 'nos', 'com', 'ou', 'que'
        ]
        # TODO: Deixar o 'job_characteristics' dinâmico.
        self.job_characteristics = {
            "technologies": ["python", "react", "node", "typescript", "react native"],
            "language": {"inglês": ["avançado", "fluente"]},
            "level": ["sênior", "pleno", "júnior"]
        }

    def start(self):
        list_result = self.__get_words()
        score_dict = self.__weighted_calculation(list_result)
        self.print_result(score_dict)
        print(f"\n{bcolors.GREEN}Calculo ponderado efetuado!{bcolors.ENDC}")

    def print_result(self, score_dict):
        print(f"{bcolors.HEADER}### DICT FILTER ####{bcolors.ENDC}\n")
        print(json.dumps(self.job_characteristics, indent=4, ensure_ascii=False))
        print(f"{bcolors.HEADER}### RESULT SCORES ####{bcolors.ENDC}\n")
        result = sorted(score_dict, key=lambda d: d['scores']['media'], reverse=True)
        color = None
        msg = None
        for item in result:
            media = item["scores"]["media"]
            if media < 25: # Ruim
                color = bcolors.RED
                msg = "Ruim"
            elif 25 < media < 50: # Ok
                color = bcolors.ORANGE
                msg = "Ok..."
            elif 50 < media < 75: # Bom
                color = bcolors.YELLOW
                msg = "Bom!"
            elif media > 75: # Ótimo
                color = bcolors.GREEN
                msg = "Ótimo!!!"
            media_text = f'{bcolors.BOLD}{color}{item["scores"]["media"]}{bcolors.ENDC}{bcolors.ENDC}'
            print(f'[{media_text}] {bcolors.UNDERLINE}{bcolors.BOLD}{msg}{bcolors.ENDC}{bcolors.ENDC} - {item["search"].url_profile}')
            print(json.dumps(item["scores"], indent=4, ensure_ascii=False))
            print("\n")

    def __bag_of_words(self, text):
        text_list = list()
        if text:
            text_list = text.lower().split()
            for idx, item in enumerate(text_list):
                for ignore_char in self.ignore_chars:
                    text_list[idx] = text_list[idx].replace(ignore_char, "").strip()
            for idx, item in enumerate(text_list):
                if text_list[idx] in self.ignore_propositions:
                    del text_list[idx]
        return text_list

    def __calculate_time(self, anos, meses):
        result = (anos * 12) + meses
        return result

    def __word_subtitle(self, profile_bag_of_words, profile):
        profile_bag_of_words["subtitle"] = self.__bag_of_words(profile.subtitle)
        return profile_bag_of_words

    def __word_about(self, profile_bag_of_words, profile):
        profile_bag_of_words["about"] = self.__bag_of_words(profile.about)
        return profile_bag_of_words

    def __word_experiences(self, profile_bag_of_words, profile):
        profile_bag_of_words["experiences"] = list()
        for experiences in profile.experiences:
            exp = {
                "descricao": list(),
                "cargo": list(),
                "tempo": 0.0
            }
            anos = 0
            meses = 0
            for carrer in experiences:
                exp["descricao"].extend(self.__bag_of_words(carrer.descricao))
                exp["cargo"].extend(self.__bag_of_words(carrer.cargo))
                anos += carrer.anos if carrer.anos else 0
                meses += carrer.meses if carrer.meses else 0
            exp["tempo"] = self.__calculate_time(anos, meses)
            profile_bag_of_words["experiences"].append(exp)
        return profile_bag_of_words

    def __word_certifications(self, profile_bag_of_words, profile):
        profile_bag_of_words["certifications"] = list()
        for certifications in profile.certifications:
            profile_bag_of_words["certifications"].extend(self.__bag_of_words(certifications.titulo))
        return profile_bag_of_words

    def __word_education(self, profile_bag_of_words, profile):
        profile_bag_of_words["education"] = list()
        for education in profile.education:
            profile_bag_of_words["education"].extend(self.__bag_of_words(education.level))
        return profile_bag_of_words

    def __word_skills(self, profile_bag_of_words, profile):
        profile_bag_of_words["skills"] = list()
        for skills in profile.skills:
            profile_bag_of_words["skills"].append(skills.__dict__)
        profile_bag_of_words["skills"] = sorted(profile_bag_of_words["skills"], key=itemgetter('verify', 'indications'))
        return profile_bag_of_words

    def __word_languages(self, profile_bag_of_words, profile):
        profile_bag_of_words["languages"] = list()
        for languages in profile.languages:
            profile_bag_of_words["languages"].append(languages.__dict__)
        return profile_bag_of_words

    def __get_words(self):
        search_list = SearchDao(self.database).select_search_person_id_is_not_null()
        list_ids = [search.person_id for search in search_list]
        list_result = list()
        for idx, person_id in enumerate(list_ids):
            profile = PersonDao(database=self.database).select_people_by_id(person_id)
            if profile:
                search = search_list[idx]
                profile_bag_of_words = dict()
                profile_bag_of_words["search"] = search
                profile_bag_of_words = self.__word_subtitle(profile_bag_of_words, profile)
                profile_bag_of_words = self.__word_about(profile_bag_of_words, profile)
                profile_bag_of_words = self.__word_experiences(profile_bag_of_words, profile)
                profile_bag_of_words = self.__word_certifications(profile_bag_of_words, profile)
                profile_bag_of_words = self.__word_education(profile_bag_of_words, profile)
                profile_bag_of_words = self.__word_skills(profile_bag_of_words, profile)
                profile_bag_of_words = self.__word_languages(profile_bag_of_words, profile)
                list_result.append(profile_bag_of_words)
        return list_result

    def __weighted_calculation(self, list_result):
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
        for idx, result in enumerate(list_result):
            score_dict = self.__create_dict_score()

            for key, value in score_dict["technologies"].items():
                score_dict = self.__set_time_experiences_descricao(result, score_dict, "technologies", key)
                score_dict = self.__set_score_skills(result, score_dict, "technologies", key)
                score_dict = self.__set_score_subtitle(result, score_dict, "technologies", key)
                score_dict = self.__set_score_about(result, score_dict, "technologies", key)
                score_dict = self.__set_score_certifications(result, score_dict, "technologies", key)

            for key, value in score_dict["language"].items():
                score_dict = self.__set_score_languages(result, score_dict, "language", key)
                score_dict = self.__set_score_subtitle(result, score_dict, "language", key)
                score_dict = self.__set_score_about(result, score_dict, "language", key)
                score_dict = self.__set_score_skills(result, score_dict, "language", key)
                score_dict = self.__set_score_certifications(result, score_dict, "language", key)

            score_dict = self.__set_score_education(result, score_dict)
            score_dict = self.set_score_experiences_cargo(result, score_dict, "level")
            score_dict["technologies"] = self.__set_score_experiences(score_dict["technologies"])
            list_result[idx]['scores'] = score_dict
            list_result[idx]['scores']["media"] = self.__media(score_dict)
        return list_result

    def __media(self, score_dict):
        """
        Calculo da média ponderada
        """
        max_score = self.__max_score(score_dict)
        sum_scores = self.__sum_all_scores(score_dict)
        percent_media = (sum_scores / max_score) * 100
        print(f"{bcolors.HEADER}###########################{bcolors.ENDC}")
        print(f"{bcolors.BOLD}Pontos máximo de cada chave:{bcolors.ENDC} {max_score}")
        print(f"{bcolors.BOLD}Todos os pontos por perfil:{bcolors.ENDC} {sum_scores}")
        print(f"{bcolors.BOLD}Média calculada:{bcolors.ENDC} {round(percent_media, 2)}")
        print(f"{bcolors.HEADER}###########################{bcolors.ENDC}")
        return round(percent_media, 2)

    def __sum_all_scores(self, score_dict):
        """
        Soma todos os pontos por perfil
        """
        for key, value in score_dict.items():
            max_score = 0
            for key, value in value.items():
                max_score += value["score"]
            return max_score

    def __max_score(self, score_dict, max_technology=32, max_language=32, max_level=10):
        """
        Soma todos os pontos máximo de cada chave
        """
        result_media_score = 0
        for key, value in score_dict.items():
            if key == "technologies":
                result_media_score += len(value) * max_technology
            elif key == "language":
                result_media_score += len(value) * max_language
            elif key == "level":
                result_media_score += len(value) * max_level
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

    def __set_score_subtitle(self, result, score_dict, main_key, key):
        """
        Adiciona a pontuação do subtitulo baseado nas palavras chaves.
        """
        if key in result["subtitle"]:
            score_dict[main_key][key]['score'] += 2
        return score_dict

    def __set_score_about(self, result, score_dict, main_key, key):
        """
        Adiciona a pontuação ao sobre baseado nas palavras chaves.
        """
        if key in result["about"]:
            score_dict[main_key][key]['score'] += 5
        return score_dict

    def __set_time_experiences_descricao(self, result, score_dict, main_key, key):
        """
        Faz a soma do tempo percorrendo as experiências para cada tecnologia.
        """
        for experience in result["experiences"]:
            if key in experience['descricao'] or key in experience['cargo']:
                tempo = experience["tempo"]
                score_dict[main_key][key]['tempo'] += tempo
        return score_dict

    def set_score_experiences_cargo(self, result, score_dict, key):
        """
        Verifica se existe no 'saco de palavras' as palavras 'sênior', 'pleno' e 'júnior', caso exista algum, o loop é
        interrompido, pois só é válido uma única validação buscando a experiência mais recente até a mais antiga.
        """
        senior = "sênior"
        pleno = "pleno"
        junior = "júnior"
        for experience in result["experiences"]:
            cargo = experience["cargo"]
            descricao = experience["descricao"]
            if senior in cargo or senior in descricao:
                score_dict[key][senior]["score"] += 10
                break
            elif pleno in cargo or pleno in descricao:
                score_dict[key][pleno]["score"] += 7
                break
            elif junior in cargo or junior in descricao:
                score_dict[key][junior]["score"] += 3
                break
        return score_dict
    
    def __set_score_experiences(self, technologies):
        """
        Adiciona os pontos de cada tecnologia baseado no tempo de experiência.
        """
        for key, value in technologies.items():
            tempo = value["tempo"]
            if self.zero_ano > tempo < self.um_ano:
                technologies[key]['score'] += 3
            elif self.um_ano < tempo < self.dois_anos:
                technologies[key]['score'] += 5
            elif self.dois_anos < tempo < self.tres_anos:
                technologies[key]['score'] += 7
            elif tempo > self.tres_anos:
                technologies[key]['score'] += 10
        return technologies

    def __set_score_certifications(self, result, score_dict, main_key, key):
        """
        Adiciona a pontuação dos certificados.
        """
        if key in result["certifications"]:
            score_dict[main_key][key]['score'] += 5
        return score_dict

    def __set_score_skills(self, result, score_dict, main_key, key):
        """
        Adiciona a pontuação da skill baseado nas indicações.
        """
        for skill in result["skills"]:
            if key in skill["titulo"].lower():
                indications = skill["indications"]
                verify = skill["verify"]
                if verify:
                    score_dict[main_key][key]['score'] += 10
                else:
                    if indications < 20:
                        score_dict[main_key][key]['score'] += 2
                    elif 20 < indications < 40:
                        score_dict[main_key][key]['score'] += 4
                    elif 40 < indications < 60:
                        score_dict[main_key][key]['score'] += 6
                    elif 60 < indications < 80:
                        score_dict[main_key][key]['score'] += 8
                    elif 80 < indications < 99:
                        score_dict[main_key][key]['score'] += 10
        return score_dict

    def __set_score_languages(self, result, score_dict, main_key, key):
        """
        Adiciona a pontuação do idioma baseado no nível.
        """
        for language in result["languages"]:
            if key in language["idioma"].lower():
                if language["nivel"]:
                    level = language["nivel"].lower().replace("nível", "").strip()
                    if level == "fluente ou nativo":
                        score_dict[main_key][key]['score'] += 10
                    elif level == "avançado":
                        score_dict[main_key][key]['score'] += 10
                    elif level == "intermediário":
                        score_dict[main_key][key]['score'] += 7
                    elif level == "básico a intermediário":
                        score_dict[main_key][key]['score'] += 4
                    elif level == "básico":
                        score_dict[main_key][key]['score'] += 1
        return score_dict

    def __set_score_education(self, result, score_dict):
        """
        Adiciona a pontuação baseado na educação.
        """
        for education in result["education"]:
            if education == "mestrado":
                score_dict["education"]['score'] += 10
                break
            elif education == "doutorado":
                score_dict["education"]['score'] += 10
                break
            elif education == "pós graduação" or education == "pós":
                score_dict["education"]['score'] += 8
                break
            elif education == "graduação" or education == "bacharel":
                score_dict["education"]['score'] += 7
                break
            elif education == "técnologo":
                score_dict["education"]['score'] += 5
                break
        return score_dict
