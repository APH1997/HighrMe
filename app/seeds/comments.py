from app.models import db, Comment, environment, SCHEMA
from sqlalchemy.sql import text
from random import choice


def seed_comments(users, pics):
    generic_comments = [
        'Oh YEAH!!',
        'Hey did Flickr get rid of ads?',
        'Stupendous',
        "I don't know who I'm more jealous of; you, or the camera!",
        "qerfjfapjs sorry cat on keyboard LOL",
        "I'm gonna email this to my grandson!",
        "I feel like a new man after seeing this!",
        "Good eye",
        "ChatGPT can't compete",
        "Blast off!!!",
        "Cowwabunga ROFL",
        "Houston, we have a problem",
        "Mid",
        "Hey, how do I use emojies on here?",
        "Can't believe I verify my bank pin to sign up for this",
        "I did NOT expect this picture to go so hard",
        "These colors remind me of grandpa. Miss ya, peepaw",
        "Gee whiz!",
        "Golly! What a view!",
        "Holy toledo, this ROCKS!",
        "Now, this? THIS is art",
        "This picture launched me into a spiral of existential dread.",
        "google.com how to undelete system 32",
        "Now I've seen a lotta pictures in my day, but this takes the cake",
        "Neato",
        "Does anyone else want to lick this picture?",
        "I wish MY photos came out this good. Wow!",
        "This sight might not look great, but the developer sure knows what they're doing!",
        "Good job!",
        "My brain literally cannot comprehend this",
        "Oh?",
        "First",
        "I'll drink to that",
        "Reminds me of the first time I licked a 9v battery lol",
        "I almost get swept out to sea when I was little. My dad rescued me.",
        "Get this person a raise",
        "Did an AI make this?",
        "Really? In this economy? Yeah right, buster.",
        "oh, I forgot what I was going to say",
        "Absolutely stunning work!",
        "You're an inspiration to us all.",
        "I'm in awe of your creativity.",
        "This deserves all the recognition.",
        "You have a true gift.",
        "I'm captivated by your artistry.",
        "Your talent is undeniable.",
        "You're pushing boundaries with your work.",
        "I'm honored to witness your talent.",
        "This is a masterpiece in the making.",
        "You've created something truly magical.",
        "Your attention to detail is remarkable.",
        "I'm completely blown away.",
        "You're raising the bar with your art.",
        "This is artistry at its finest.",
        "Your work leaves me breathless.",
        "You've captured the essence beautifully.",
        "I can't stop admiring your talent.",
        "This evokes so much emotion in me.",
        "You're destined for greatness.",
        "I'm privileged to experience your art.",
        "You're a true master of your craft.",
        "This speaks to my soul.",
        "Your art is thought-provoking.",
        "I'm forever grateful for your creativity.",
        "You're pushing the boundaries of art.",
        "I'm in love with your artistic style.",
        "Your work is a true feast for the eyes.",
        "This deserves a place in a gallery.",
        "You're making a significant impact.",
        "I'm in awe of your artistic vision.",
        "Your talent shines through your creations.",
        "I can't get enough of your art.",
        "You're a true virtuoso.",
        "This is a work of sheer brilliance.",
        "Your art is changing lives.",
        "You have a unique and powerful voice.",
        "I'm honored to be touched by your art.",
        "You're an artistic genius.",
        "This is beyond words, simply extraordinary.",
        "Your work resonates deeply with me.",
        "You're a true trailblazer.",
        "This is art that makes a difference.",
        "Your creativity knows no limits.",
        "I'm spellbound by your artistic expression.",
        "You're creating magic with your art.",
        "This deserves worldwide acclaim.",
        "You're a visionary in the art world.",
        "Your talent is awe-inspiring.",
        "I'm moved by your artistic genius.",
        "You're creating a legacy through your art.",
        "This is art that transcends boundaries.",
        "Your work is an inspiration to others.",
        "You're leaving an indelible mark on art.",
        "This takes my breath away.",
        "Your art has a profound impact.",
        "You're a true luminary in the art realm.",
        "This is art that touches the soul.",
        "Your talent is a gift to the world.",
        "I'm awestruck by your artistic prowess.",
        "You're forging a new path in art.",
        "This is art that sparks conversations.",
        "Your creations are pure magic.",
        "You're an artist of unparalleled talent.",
        "This is art that provokes thought.",
        "Your work is truly transformative.",
        "You're making waves in the art world.",
        "This is artistry at its most sublime.",
        "Your talent is a true treasure.",
        "I'm in complete admiration of your art.",
        "You're breathing life into your creations.",
        "This deserves the highest accolades.",
        "Your art has the power to heal.",
        "You're a true visionary artist.",
        "This is a testament to your genius.",
        "Your talent is a source of inspiration.",
        "You're creating art that touches hearts.",
        "This is art that stirs the soul.",
        "Your work is a testament to human creativity.",
        "I'm in awe of your artistic journey.",
        "You're pushing the boundaries of imagination.",
        "This is art that ignites passion.",
        "Your creations are captivating.",
        "You're an artist of extraordinary caliber.",
        "This deserves global recognition.",
        "Your art is a gift to humanity.",
        "You're redefining the art landscape.",
        "This is art that defies expectations.",
        "Your talent is simply unparalleled.",
        "I'm deeply moved by your artistic expression.",
        "You're a true pioneer in the art world.",
        "This is art that transcends time.",
        "Your work has a profound impact on others.",
        "You're forging a new era of artistry.",
        "This is art that challenges perceptions.",
        "Your creations are nothing short of extraordinary.",
        "You're a true luminary in the art realm.",
        "This deserves eternal admiration.",
        "Your artistry takes my breath away.",
        "You're a true master of your craft."
    ]

    all_comments = [Comment(
        photo=choice(pics),
        author=choice(users),
        content=comment
    ) for comment in generic_comments]

    add = [db.session.add(comment) for comment in all_comments]

    db.session.commit()
    return all_comments


def undo_comments():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.comments RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM comments"))

    db.session.commit()
