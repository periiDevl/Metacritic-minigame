import time
import requests
import pygame
from bs4 import BeautifulSoup
from langdetect import detect
import random
import io
from io import BytesIO
import concurrent.futures
from urllib.parse import urlparse
base_url = "https://www.metacritic.com/game/playstation-4/{}/user-reviews"
game_list = ["red-dead-redemption-2", "the-last-of-us-part-ii", "god-of-war", "marvels-spider-man", "detroit-become-human"]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
char_limit = 250
review_limit = 3

import random

import concurrent.futures

def get_reviews(game, headers, base_url, char_limit, review_limit):
    used_reviews = set()
    count = 0
    page_number = 1
    while True:
        url = base_url.format(game) + "?page=" + str(page_number)
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        reviews = soup.find_all("div", class_="review_content")
        if not reviews:
            break

        for i, review in enumerate(reviews):
            blurb = review.find("span", class_="blurb blurb_expanded")
            score = review.find("div", class_="review_grade")
            if blurb:
                text = blurb.text.strip()
                if detect(text) == "en" and text not in used_reviews and len(text) <= char_limit:
                    if score:
                        font = pygame.font.Font(None, 22)
                        fontScore = pygame.font.Font(None, 55)
                        score_value = float(score.text.strip())
                        if 0 <= score_value <= 3 or 8 <= score_value <= 10:
                            used_reviews.add(text)
                            count += 1
                            score_text = fontScore.render(str(score_value), True, (255, 255, 255))

                            words = text.split(" ")
                            lines = []
                            line = ""
                            for word in words:
                                if font.size(line + " " + word)[0] <= screen.get_width():
                                    line += " " + word
                                else:
                                    lines.append(line)
                                    line = word
                            if line:
                                lines.append(line)

                            y_offset = -100 + count * 130
                            for line in lines:
                                review_text = font.render(line, True, (0, 0, 0))
                                screen.blit(review_text, (0, y_offset))
                                y_offset += font.get_height()

                            if (score_value > 5):
                                pygame.draw.rect(screen, (102, 204, 51), (920, y_offset, 75,75 ), 0, 70)
                                screen.blit(score_text, (920, y_offset + 20))
                            elif (score_value < 5):
                                pygame.draw.rect(screen, (255, 0, 0), (920, y_offset, 75, 75 ), 0, 70)
                                screen.blit(score_text, (920, y_offset + 20))

                            y_offset += font.get_height()

                            if count >= review_limit:
                                return


                    else:
                        #print("No score found for this review. Review: " + text)
                        review_text = font.render(text, True, (0, 0, 0))

        page_number += 1



def get_game_cover(game):
    url = base_url.format(game)
    page = requests.get(url, headers=headers).content
    soup = BeautifulSoup(page, 'html.parser')
    cover_img = soup.find("img", class_="product_image")
    if cover_img:
        cover_url = cover_img["src"]
        cover_image = requests.get(cover_url).content
        return pygame.image.load(BytesIO(cover_image))
    return None

def get_game_covers_concurrently(games):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(get_game_cover, game) for game in games]
        
        return [result.result() for result in concurrent.futures.as_completed(results)]

def display_image(game, x, y, scale = 1.13):
    cover_image = get_game_cover(game)
    if cover_image:
        cover_image = pygame.transform.scale(cover_image, (int(cover_image.get_width() * scale), int(cover_image.get_height() * scale)))
        screen.blit(cover_image, (x, y))
        return cover_image.get_rect().move(x, y)
    return None


    
    
    


    
pygame.init()
screen = pygame.display.set_mode((1000, 600), pygame.NOFRAME)
pygame.display.set_caption("Metacritic game")

positions = [440 - 130, 440, 440 + 130]
realgame_rect = pygame.Rect(positions[0], 0, 200, 200)
fakegame1_rect = pygame.Rect(positions[1], 0, 200, 200)
fakegame2_rect = pygame.Rect(positions[2], 0, 200, 200)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False
                
            if event.key == pygame.K_SPACE:
                realgame = random.choice(game_list)
                print("Random game selected: ", realgame)

                fakegame1 = random.choice(game_list)
                while fakegame1 == realgame:
                    fakegame1 = random.choice(game_list)
                print("Fake game selected: ", fakegame1)

                fakegame2 = random.choice(game_list)
                while fakegame2 == realgame or fakegame2 == fakegame1:
                    fakegame2 = random.choice(game_list)
                print("Fake game selected: ", fakegame2)

                color = (255, 255, 255)
                screen.fill(color)
                pygame.display.update()

                pygame.draw.rect(screen, (246,246,246),  (0,0, 1000, 1000 ), 0, 5)
                pygame.draw.rect(screen, (217,217,217),  (0,0, 1000, 1000 ), 2, 5)


                pygame.draw.rect(screen, (255,255,255), (0, 20, 1000, 120 ), 0, 10)
                pygame.draw.rect(screen, (255,255,255), (0, 150, 1000, 120 ), 0, 10)
                pygame.draw.rect(screen, (255,255,255),  (0, 280, 1000, 120 ), 0, 10)

                pygame.draw.rect(screen, (217,217,217), (0, 20, 1000, 120 ), 2, 10)
                pygame.draw.rect(screen, (217,217,217), (0, 150, 1000, 120 ), 2, 10)
                pygame.draw.rect(screen, (217,217,217),  (0, 280, 1000, 120 ), 2, 10)

                

                
                get_reviews(realgame, headers, base_url, char_limit, review_limit)

                
                


                pygame.draw.rect(screen, (255, 255, 255), (290, 445, 410, 370 ), 0, 10)
                pygame.draw.rect(screen, (217, 217, 217), (290, 445, 410, 370 ), 1, 10)
                
                random.shuffle(positions)

                realgame_rect = display_image(realgame, positions[0], 460)
                fakegame1_rect = display_image(fakegame1, positions[1], 460)
                fakegame2_rect = display_image(fakegame2, positions[2], 460)
                pygame.display.flip()
                pygame.display.update()
                print("LOADED")
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if realgame_rect.collidepoint(mouse_pos):
                print("Mouse is hovering over realgame cover")
            elif fakegame1_rect.collidepoint(mouse_pos):
                print("Mouse is hovering over fakegame1 cover")
            elif fakegame2_rect.collidepoint(mouse_pos):
                print("Mouse is hovering over fakegame2 cover")


pygame.quit()