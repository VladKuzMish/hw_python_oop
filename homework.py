from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(*asdict(self).values())


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
            f'Определите get_spent_calories, в {(self.__class__.__name__)}'
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

    SPEED_MULTIPLIER = 18
    SPEED_MULTIPLIER_2 = 20

    def get_spent_calories(self) -> float:
        """Расчитываем коллории, затраченные на тренировку."""
        return (
            (self.SPEED_MULTIPLIER
             * self.get_mean_speed() - self.SPEED_MULTIPLIER_2)
            * self.weight / self.M_IN_KM * self.duration * self.M_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WALKING_MULTIPLIER = 0.035
    WALKING_MULTIPLIER_2 = 2
    WALKING_MULTIPLIER_3 = 0.029

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
            self.WALKING_MULTIPLIER * self.weight
            + (self.get_mean_speed() ** self.WALKING_MULTIPLIER_2
               // self.height)
            * self.WALKING_MULTIPLIER_3 * self.weight
        ) * self.duration * self.M_IN_HOUR

        return walking_1


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    SWIMING_MULTIPLIER = 1.1
    SWIMING_MULTIPLIER_2 = 2

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
            (self.get_mean_speed() + self.SWIMING_MULTIPLIER)
            * self.SWIMING_MULTIPLIER_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    try:
        return WORKOUTS.get(workout_type)(*data)
    except ValueError:
        print('Тренировки нет в словаре')


WORKOUTS: Dict[str, Type[Training]] = {
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
