from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

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

    def __init__(
            self,
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
        raise NotImplementedError(
            'Определите get_spent_calories, в %s.' %
            (self.__class__.__name__)
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    S_MULTIPLIER = 18
    S_MULTIPLIER_2 = 20

    def get_spent_calories(self) -> float:
        """Расчитываем коллории, затраченные на тренировку."""
        return (
            (self.S_MULTIPLIER * self.get_mean_speed() - self.S_MULTIPLIER_2)
            * self.weight / self.M_IN_KM * (self.duration * self.M_IN_HOUR)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_WALK_1 = 0.035
    COEF_WALK_2 = 2
    COEF_WALK_3 = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> float:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчитываем коллории, затраченные на тренировку."""
        walking_1 = (
            self.COEF_WALK_1 * self.weight
            + (self.get_mean_speed() ** self.COEF_WALK_2 // self.height)
            * self.COEF_WALK_3
            * self.weight) * (self.duration * self.M_IN_HOUR)
        return walking_1


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEF_SWIM_1 = 1.1
    COEF_SWIM_2 = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool,
            count_pool: int,
    ) -> float:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Расчитываем среднюю скорость тренировки."""
        mean_speed = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Расчитываем коллории, затраченные на тренировку."""
        return (
            (self.get_mean_speed() + self.COEF_SWIM_1)
            * self.COEF_SWIM_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    return WORKOUTS.get(workout_type)(*data)


WORKOUTS = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def main(training: Training) -> None:
    """Главная функция."""
    return print(f'{training.show_training_info().get_message()}')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
