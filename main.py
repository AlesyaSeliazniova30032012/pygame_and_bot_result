import pygame
import telebot
import sys

import os
from dotenv import load_dotenv, find_dotenv

from markup import kb

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('token'))

pygame.init()
fps = 40
pygame.display.set_caption('БАТЛ КВАДРАТОВ')
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()


class RunKwadr(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.direction = None
        self.image = pygame.Surface((70, 70))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 300)
        self.speed = 10

    def update(self):
        self.direction = {'x': 0}

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.direction['x'] = 1
            self.rect.x += self.speed


class StaticKwadr(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70, 70))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (300, 300)


all_sprites = pygame.sprite.Group()
kwadr1 = RunKwadr()
kwadr2 = StaticKwadr()
all_sprites.add(kwadr1, kwadr2)
pygame.display.update()


def collide_bah():
    hits = kwadr2.rect.colliderect(kwadr1.rect)
    if hits:
        kwadr2.rect.x += kwadr1.speed * kwadr1.direction.get('x')


def collide_border():
    if kwadr2.rect.x >= 650:
        kwadr2.speed = 0
        coordinate = f'{kwadr2.rect.topleft}, {kwadr2.rect.topright}, {kwadr2.rect.bottomleft}, {kwadr2.rect.bottomright}'

        @bot.message_handler(commands=['start'])
        def start(message):
            bot.send_message(message.chat.id, text='Привет, чем могу помочь?', reply_markup=kb)

        @bot.callback_query_handler(func=lambda call: True)
        def call_inline(call):
            if call.data == 'coordinate':
                bot.send_message(call.message.chat.id, coordinate)
                bot.send_message(call.message.chat.id, text='Хочешь теперь скрин начала игры?', reply_markup=kb)

            if call.data == 'scrin':
                img = open('img.png', 'rb')
                bot.send_photo(call.message.chat.id, photo=img, caption='Скрин начала игры')
                bot.send_message(call.message.chat.id, text='Хочешь теперь узнать координаты неубежавшего квадрата?',
                                 reply_markup=kb)

        pygame.quit()
        bot.polling(none_stop=True)


while True:
    screen.fill((0, 0, 0))
    clock.tick(fps)
    all_sprites.update()
    all_sprites.draw(screen)

    collide_bah()
    collide_border()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
