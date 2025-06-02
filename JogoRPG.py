from typing import Optional, Dict, List
import random


class Personagem:
    def __init__(self, nome: str, nivel: int, hp_max: int, ataque: int):
        self._nome = nome
        self._nivel = nivel
        self._hp_max = hp_max
        self._hp = hp_max
        self._ataque = ataque

    @property
    def nome(self):
        return self._nome

    @property
    def nivel(self):
        return self._nivel

    @nivel.setter
    def nivel(self, valor):
        if valor > 0:
            self._nivel = valor

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, valor):
        if 0 <= valor <= self._hp_max:
            self._hp = valor
        elif valor < 0:
            self._hp = 0
        else:
            self._hp = self._hp_max

    @property
    def hp_max(self):
        return self._hp_max

    @property
    def ataque(self):
        return self._ataque

    def esta_vivo(self):
        return self._hp > 0

    def receber_dano(self, dano: int):
        self.hp = self._hp - dano

    def atacar_alvo(self, alvo: 'Personagem'):
        print(f"{self.nome} ataca {alvo.nome} causando {self.ataque} de dano.")
        alvo.receber_dano(self.ataque)


class Jogador(Personagem):
    def __init__(self, nome: str):
        super().__init__(nome, nivel=1, hp_max=100, ataque=10)
        self.arvore_de_habilidades = ArvoreDeHabilidades()

    def subir_de_nivel(self):
        self.nivel += 1
        self._hp_max += 20
        self.hp = self._hp_max
        self._ataque += 5
        print(f"{self.nome} subiu para o nível {self.nivel}!")

    def aprender_habilidade(self, habilidade: str):
        if self.arvore_de_habilidades.aprender(habilidade):
            print(f"{self.nome} aprendeu a habilidade: {habilidade}")
        else:
            print(f"Não foi possível aprender {habilidade} (pré-requisitos não cumpridos ou já aprendida).")

    def rolar_d20(self) -> int:
        roll = random.randint(1, 20)
        print(f"{self.nome} rolou um D20 e tirou: {roll}")
        return roll

    def atacar_alvo_com_d20(self, alvo: 'Personagem', roll: Optional[int] = None):
        print('\033[34m=======================\033[0m')
        if roll is None:
            roll = self.rolar_d20()

        if 1 <= roll <= 5:
            print("Ataque sem efeito.")
            dano = 0
        elif 6 <= roll <= 10:
            dano = int(self.ataque * 0.5)
            print(f"Ataque fraco! Dano: {dano}")
        elif 11 <= roll <= 15:
            dano = self.ataque
            print(f"Ataque forte! Dano: {dano}")
        elif 16 <= roll <= 19:
            dano = int(self.ataque * 1.5)
            print(f"Ataque muito forte! Dano: {dano}")
        else:  # 20
            dano = self.ataque * 2
            print(f"CRÍTICO! Dano: {dano}")

        alvo.receber_dano(dano)
        print('=======================')




class Inimigo(Personagem):
    def __init__(self, nome: str, nivel: int):
        hp_max = 30 + (nivel - 1) * 20
        ataque = 8 + (nivel - 1) * 5
        super().__init__(nome, nivel, hp_max, ataque)

    def rolar_d20(self) -> int:
        roll = random.randint(1, 20)
        print(f"{self.nome} rolou um D20 e tirou: {roll}")
        return roll

    def atacar_alvo_com_d20(self, alvo: 'Personagem', roll: Optional[int] = None):
        if roll is None:
            roll = self.rolar_d20()

        if 1 <= roll <= 5:
            print("Ataque do inimigo sem efeito.")
            dano = 0
        elif 6 <= roll <= 10:
            dano = int(self.ataque * 0.5)
            print(f"Ataque fraco do inimigo! Dano: {dano}")
        elif 11 <= roll <= 15:
            dano = self.ataque
            print(f"Ataque forte do inimigo! Dano: {dano}")
        elif 16 <= roll <= 19:
            dano = int(self.ataque * 1.5)
            print(f"Ataque muito forte do inimigo! Dano: {dano}")
        else:  # 20
            dano = self.ataque * 2
            print(f"CRÍTICO do inimigo! Dano: {dano}")

        alvo.receber_dano(dano)
        print('\033[31m=======================\033[0m')




# Inicio da Arvore Binaria para filtrar os inimigos por nivel de dificuldade

class NodoInimigo:
    def __init__(self, inimigo: Inimigo):
        self.inimigo = inimigo
        self.esquerda: Optional['NodoInimigo'] = None
        self.direita: Optional['NodoInimigo'] = None


class ArvoreBinariaDeBuscaInimigos:
    def __init__(self):
        self.raiz: Optional[NodoInimigo] = None

    def inserir(self, inimigo: Inimigo):
        if self.raiz is None:
            self.raiz = NodoInimigo(inimigo)
        else:
            self._inserir_nodo(self.raiz, inimigo)

    def _inserir_nodo(self, nodo: NodoInimigo, inimigo: Inimigo):
        if inimigo.nivel < nodo.inimigo.nivel:
            if nodo.esquerda is None:
                nodo.esquerda = NodoInimigo(inimigo)
            else:
                self._inserir_nodo(nodo.esquerda, inimigo)
        else:
            if nodo.direita is None:
                nodo.direita = NodoInimigo(inimigo)
            else:
                self._inserir_nodo(nodo.direita, inimigo)

    def buscar_por_nivel(self, nivel: int) -> Optional[Inimigo]:
        return self._buscar_nodo(self.raiz, nivel)

    def _buscar_nodo(self, nodo: Optional[NodoInimigo], nivel: int) -> Optional[Inimigo]:
        if nodo is None:
            return None
        if nivel == nodo.inimigo.nivel:
            return nodo.inimigo
        elif nivel < nodo.inimigo.nivel:
            return self._buscar_nodo(nodo.esquerda, nivel)
        else:
            return self._buscar_nodo(nodo.direita, nivel)


# Inicio do Grafo para a arvore de habildiades

class ArvoreDeHabilidades:
    def __init__(self):
        # Grafo representando a skill tree (lista de adjacências)
        self.grafo: Dict[str, List[str]] = {
            "Raiz": ["Golpe", "Bloqueio"],
            "Golpe": ["Golpe Poderoso"],
            "Bloqueio": ["Investida com Escudo"],
            "Golpe Poderoso": [],
            "Investida com Escudo": []
        }
        self.habilidades_aprendidas = {"Raiz"}

    def pode_aprender(self, habilidade: str) -> bool:
        for pai, filhos in self.grafo.items():
            if habilidade in filhos and pai not in self.habilidades_aprendidas:
                return False
        return True

    def aprender(self, habilidade: str) -> bool:
        if habilidade in self.habilidades_aprendidas:
            return False
        if habilidade not in self.grafo:
            return False
        if self.pode_aprender(habilidade):
            self.habilidades_aprendidas.add(habilidade)
            return True
        return False


def interagir_com_arvore_de_habilidades(jogador: Jogador):
    while True:
        print("\n💡 Árvore de Habilidades:")
        for habilidade, filhos in jogador.arvore_de_habilidades.grafo.items():
            status = "✅" if habilidade in jogador.arvore_de_habilidades.habilidades_aprendidas else "❌"
            prereqs = [pai for pai, kids in jogador.arvore_de_habilidades.grafo.items() if habilidade in kids]
            prereq_status = "OK" if all(pr in jogador.arvore_de_habilidades.habilidades_aprendidas for pr in prereqs) else "Bloqueado"
            print(f" - {habilidade}: {status} (Pré-requisitos: {prereqs if prereqs else 'Nenhum'}) [{prereq_status}]")

        escolha = input("Digite o nome da habilidade que deseja aprender (ou 'sair' para continuar): ").strip()
        if escolha.lower() == 'sair':
            break
        elif escolha not in jogador.arvore_de_habilidades.grafo:
            print("⚠️ Habilidade inválida. Tente novamente.")
            continue
        elif escolha in jogador.arvore_de_habilidades.habilidades_aprendidas:
            print("⚠️ Você já aprendeu essa habilidade.")
            continue
        elif not jogador.arvore_de_habilidades.pode_aprender(escolha):
            print("⚠️ Você não cumpriu os pré-requisitos para essa habilidade.")
            continue

        jogador.aprender_habilidade(escolha)


def main():
    jogador = Jogador("Herói")

    arvore_inimigos = ArvoreBinariaDeBuscaInimigos()
    arvore_inimigos.inserir(Inimigo("Goblin", 1))
    arvore_inimigos.inserir(Inimigo("Orc", 3))
    arvore_inimigos.inserir(Inimigo("Troll", 2))

    print("=== RPG Simples com Árvore Binária de Busca, Skill Tree com grafos e D20 ===\n")

    while jogador.esta_vivo():
        inimigo = arvore_inimigos.buscar_por_nivel(jogador.nivel)
        if inimigo is None:
            print("Não há inimigos para o seu nível. Você venceu o jogo!")
            break

        print(f"Inimigo encontrado: {inimigo.nome} (Nível {inimigo.nivel})")

        while jogador.esta_vivo() and inimigo.esta_vivo():
            input("Pressione ENTER para atacar...")  # interação do usuário fora do método
            jogador.atacar_alvo_com_d20(inimigo)
            if inimigo.esta_vivo():
                inimigo.atacar_alvo_com_d20(jogador)
            else:
                print(f"{inimigo.nome} foi derrotado!")
                jogador.subir_de_nivel()

                interagir_com_arvore_de_habilidades(jogador)
                break

        if not jogador.esta_vivo():
            print(f"{jogador.nome} morreu. Fim de jogo.")
            break

        print("--------------\n")


if __name__ == "__main__":
    main()
