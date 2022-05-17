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
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.'
                    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

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

    WEIGHT_MULTIPLIER = 0.035
    GET_MEAN_SPEED = 2
    WEIGHT_MULTIPLIER_2 = 0.029

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
        return (
            self.WEIGHT_MULTIPLIER * self.weight
            + (self.get_mean_speed() ** self.GET_MEAN_SPEED
               // self.height)
            * self.WEIGHT_MULTIPLIER_2 * self.weight
        ) * self.duration * self.M_IN_HOUR


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    GET_MEAN_SPEED_2 = 1.1
    WEIGHT_MULTIPLIER_2 = 2

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
        return(
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Расчитываем коллории, затраченные на тренировку."""
        return (
            (self.get_mean_speed() + self.GET_MEAN_SPEED_2)
            * self.WEIGHT_MULTIPLIER_2 * self.weight
        )


WORKOUTS: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    try:
        return WORKOUTS.get(workout_type)(*data)
    except ValueError:
        print('Тренировки нет в словаре')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
