import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import random
import math
from itertools import combinations

class LotteryAnalyzer:
    def __init__(self):
        self.historical_results = []  # Lista de resultados históricos
        self.max_number = 43  # Número máximo para los 5 números principales
        self.hot_number_max = 16  # Número máximo para el número caliente
        
    def add_result(self, regular_numbers, hot_number):
        """Añade un resultado a los datos históricos."""
        if len(regular_numbers) != 5:
            raise ValueError("Se necesitan exactamente 5 números regulares")
        
        # Validar rango de números regulares
        for num in regular_numbers:
            if num < 0 or num > self.max_number:
                raise ValueError(f"Los números regulares deben estar entre 0 y {self.max_number}")
        
        # Validar número caliente
        if hot_number < 1 or hot_number > self.hot_number_max:
            raise ValueError(f"El número caliente debe estar entre 1 y {self.hot_number_max}")
            
        # Verificar que no haya duplicados en números regulares
        if len(set(regular_numbers)) != len(regular_numbers):
            raise ValueError("Los números regulares no deben repetirse")
            
        self.historical_results.append({
            'regular': sorted(regular_numbers),
            'hot': hot_number
        })
        
    def analyze_frequency(self):
        """Analiza la frecuencia de aparición de números."""
        regular_frequency = Counter()
        hot_frequency = Counter()
        
        for result in self.historical_results:
            regular_frequency.update(result['regular'])
            hot_frequency.update([result['hot']])
            
        return {
            'regular': regular_frequency,
            'hot': hot_frequency
        }
    
    def analyze_patterns(self):
        """Analiza patrones en los resultados."""
        if len(self.historical_results) < 2:
            return "No hay suficientes datos para analizar patrones"
            
        patterns = {
            'sum_regular': [],  # Suma de números regulares
            'odd_even_ratio': [],  # Proporción de impares vs pares
            'range_distribution': [],  # Distribución en rangos
            'consecutive_numbers': [],  # Presencia de números consecutivos
            'hot_correlation': []  # Correlación con número caliente
        }
        
        for result in self.historical_results:
            # Suma de números regulares
            patterns['sum_regular'].append(sum(result['regular']))
            
            # Proporción de impares vs pares
            odd_count = sum(1 for num in result['regular'] if num % 2 == 1)
            patterns['odd_even_ratio'].append(odd_count / 5)
            
            # Distribución en rangos
            ranges = [0, 0, 0, 0]  # 0-10, 11-21, 22-32, 33-43
            for num in result['regular']:
                ranges[min(3, num // 11)] += 1
            patterns['range_distribution'].append(ranges)
            
            # Números consecutivos
            has_consecutive = False
            sorted_nums = sorted(result['regular'])
            for i in range(len(sorted_nums) - 1):
                if sorted_nums[i + 1] - sorted_nums[i] == 1:
                    has_consecutive = True
                    break
            patterns['consecutive_numbers'].append(has_consecutive)
            
            # Correlación con número caliente
            in_regular = result['hot'] in result['regular']
            patterns['hot_correlation'].append(in_regular)
            
        return patterns
    
    def chaos_theory_analysis(self):
        """Aplica conceptos básicos de teoría del caos para detectar comportamiento no lineal."""
        if len(self.historical_results) < 3:
            return "No hay suficientes datos para análisis de caos"
            
        # Análisis de Lyapunov simplificado
        total_numbers = []
        for result in self.historical_results:
            total_numbers.extend(result['regular'])
            total_numbers.append(result['hot'])
            
        differences = []
        for i in range(1, len(total_numbers)):
            differences.append(abs(total_numbers[i] - total_numbers[i-1]))
            
        if not differences:
            return "No se pueden calcular diferencias"
            
        lyapunov_estimate = sum(math.log(abs(d)) if d != 0 else 0 for d in differences) / len(differences)
        
        return {
            'lyapunov_estimate': lyapunov_estimate,
            'is_chaotic': lyapunov_estimate > 0
        }
        
    def enigma_inspired_analysis(self):
        """Análisis inspirado en el concepto de la máquina Enigma (rotación y sustitución)."""
        if not self.historical_results:
            return "No hay datos para analizar"
            
        # Crear un "rotor" basado en los últimos resultados
        last_results = self.historical_results[-1]['regular']
        
        # Crear una transformación basada en la suma de los números anteriores
        transformation = {}
        for i in range(self.max_number + 1):
            # Transformación inspirada en el rotor de Enigma
            transformed = (i + sum(last_results)) % (self.max_number + 1)
            transformation[i] = transformed
            
        # Aplicar transformación a los resultados históricos para buscar patrones
        transformed_results = []
        for result in self.historical_results:
            transformed = [transformation[num] for num in result['regular']]
            transformed_results.append(transformed)
            
        return {
            'transformation': transformation,
            'transformed_results': transformed_results
        }
    
    def predict_next_result(self, num_predictions=5):
        """Genera predicciones para el próximo resultado."""
        if len(self.historical_results) < 3:
            return "Se necesitan al menos 3 resultados históricos para hacer predicciones"
            
        # Obtener análisis
        frequency = self.analyze_frequency()
        patterns = self.analyze_patterns()
        
        # 1. Predicción basada en frecuencia
        most_common_regular = [num for num, _ in frequency['regular'].most_common(10)]
        most_common_hot = [num for num, _ in frequency['hot'].most_common(3)]
        
        # 2. Predicción basada en patrones
        avg_sum = sum(patterns['sum_regular']) / len(patterns['sum_regular'])
        avg_odd_ratio = sum(patterns['odd_even_ratio']) / len(patterns['odd_even_ratio'])
        
        # 3. Predicción basada en rango de distribución
        avg_range = [0, 0, 0, 0]
        for dist in patterns['range_distribution']:
            for i in range(4):
                avg_range[i] += dist[i]
        avg_range = [r / len(patterns['range_distribution']) for r in avg_range]
        
        # Generar predicciones combinando todos los métodos
        predictions = []
        
        for _ in range(num_predictions):
            # Equilibrar entre números frecuentes y menos frecuentes
            candidate_numbers = set()
            
            # Incluir algunos números frecuentes
            for _ in range(3):
                if most_common_regular:
                    candidate_numbers.add(random.choice(most_common_regular))
            
            # Incluir números de diferentes rangos según distribución histórica
            nums_needed = 5 - len(candidate_numbers)
            ranges_to_pick = []
            for i in range(4):
                ranges_to_pick.extend([i] * max(1, int(avg_range[i] * 2)))
                
            for _ in range(nums_needed):
                if len(candidate_numbers) >= 5:
                    break
                    
                # Elegir un rango basado en la distribución histórica
                range_idx = random.choice(ranges_to_pick)
                min_val = range_idx * 11
                max_val = min(self.max_number, (range_idx + 1) * 11 - 1)
                
                attempts = 0
                while attempts < 10:  # Evitar bucle infinito
                    new_num = random.randint(min_val, max_val)
                    if new_num not in candidate_numbers:
                        candidate_numbers.add(new_num)
                        break
                    attempts += 1
            
            # Asegurarse de tener 5 números únicos
            while len(candidate_numbers) < 5:
                new_num = random.randint(0, self.max_number)
                candidate_numbers.add(new_num)
                
            # Convertir a lista y ordenar
            final_numbers = sorted(list(candidate_numbers)[:5])
            
            # Número caliente
            hot_number = random.choice(most_common_hot) if most_common_hot else random.randint(1, self.hot_number_max)
            
            predictions.append({
                'regular': final_numbers,
                'hot': hot_number
            })
            
        return predictions
    
    def visualize_data(self):
        """Visualiza los datos históricos para análisis."""
        if not self.historical_results:
            return "No hay datos para visualizar"
            
        # Frecuencia de números regulares
        frequencies = [0] * (self.max_number + 1)
        for result in self.historical_results:
            for num in result['regular']:
                frequencies[num] += 1
                
        # Frecuencia de números calientes
        hot_frequencies = [0] * (self.hot_number_max + 1)
        for result in self.historical_results:
            hot_frequencies[result['hot']] += 1
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Gráfico de frecuencia de números regulares
        x = range(self.max_number + 1)
        ax1.bar(x, frequencies)
        ax1.set_title('Frecuencia de Números Regulares')
        ax1.set_xlabel('Número')
        ax1.set_ylabel('Frecuencia')
        
        # Gráfico de frecuencia de números calientes
        x_hot = range(1, self.hot_number_max + 1)
        ax2.bar(x_hot, hot_frequencies[1:])
        ax2.set_title('Frecuencia de Números Calientes')
        ax2.set_xlabel('Número')
        ax2.set_ylabel('Frecuencia')
        
        plt.tight_layout()
        plt.show()
        
        return "Visualización generada"

# Ejemplo de uso del sistema
def main():
    print("\n===== SISTEMA DE ANÁLISIS Y PREDICCIÓN DE RESULTADOS =====\n")
    analyzer = LotteryAnalyzer()
    
    # Solicitar al usuario los resultados de las últimas 3 semanas
    num_weeks = 3
    for i in range(num_weeks):
        print(f"\nSemana {i+1}:")
        valid_input = False
        while not valid_input:
            try:
                regular_input = input("Ingresa los 5 números regulares separados por guiones (ej: 05-07-23-38-41): ")
                regular_numbers = [int(num) for num in regular_input.split('-')]
                
                hot_input = input("Ingresa el número caliente (1-16): ")
                hot_number = int(hot_input)
                
                analyzer.add_result(regular_numbers, hot_number)
                valid_input = True
                print("Resultado registrado correctamente.")
            except ValueError as e:
                print(f"Error: {e}. Intenta nuevamente.")
    
    # Realizar análisis
    print("\n===== ANÁLISIS DE DATOS =====")
    
    # Análisis de frecuencia
    frequency = analyzer.analyze_frequency()
    print("\nFrecuencia de números regulares (top 10):")
    for num, freq in frequency['regular'].most_common(10):
        print(f"Número {num:02d}: {freq} veces")
        
    print("\nFrecuencia de números calientes:")
    for num, freq in frequency['hot'].most_common():
        print(f"Número {num:02d}: {freq} veces")
    
    # Análisis de patrones
    patterns = analyzer.analyze_patterns()
    print("\nAnálisis de patrones:")
    print(f"Promedio de suma de números regulares: {sum(patterns['sum_regular'])/len(patterns['sum_regular']):.2f}")
    print(f"Proporción promedio de números impares: {sum(patterns['odd_even_ratio'])/len(patterns['odd_even_ratio']):.2f}")
    
    # Análisis inspirado en teoría del caos
    chaos = analyzer.chaos_theory_analysis()
    if isinstance(chaos, dict):
        print(f"\nIndicador de Lyapunov: {chaos['lyapunov_estimate']:.4f}")
        print(f"Sistema caótico: {'Sí' if chaos['is_chaotic'] else 'No'}")
    
    # Predicciones
    print("\n===== PREDICCIONES PARA LA PRÓXIMA SEMANA =====")
    predictions = analyzer.predict_next_result(num_predictions=3)
    
    for i, pred in enumerate(predictions):
        regular_formatted = '-'.join(f"{num:02d}" for num in pred['regular'])
        print(f"\nPredicción {i+1}:")
        print(f"Números regulares: {regular_formatted}")
        print(f"Número caliente: {pred['hot']:02d}")
    
    # Generar visualización
    print("\n¿Deseas visualizar los datos? (s/n)")
    if input().lower() == 's':
        analyzer.visualize_data()
    
    print("\n===== FIN DEL ANÁLISIS =====")

if __name__ == "__main__":
    main()
