class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    M_IN_HOUR: float = 60
    action: int
    duration: float
    weight: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_1 = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_1

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    calorie_1 = 18
    calorie_2 = 20

    def get_spent_calories(self) -> float:
        return (
            (self.calorie_1 * self.get_mean_speed() - self.calorie_2)
            * self.weight / self.M_IN_KM * (self.duration * self.M_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coef_walking_1 = 0.035
    coef_walking_2 = 2
    coef_walking_3 = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> float:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        walking_1 = (
            self.coef_walking_1 * self.weight
            + (self.get_mean_speed() ** self.coef_walking_2 // self.height)
            * self.coef_walking_3
            * self.weight) * (self.duration * self.M_IN_HOUR)
        return walking_1


class Swimming(Training):
    LEN_STEP: float = 1.38
    """Тренировка: плавание."""
    coef_swiming_1 = 1.1
    coef_swiming_2 = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool,
            count_pool: int
    ) -> float:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = (
            (self.get_mean_speed() + self.coef_swiming_1)
            * self.coef_swiming_2 * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_name = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return class_name.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return print(f'{info.get_message()}')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
