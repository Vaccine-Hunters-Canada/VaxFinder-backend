from discord_webhook import DiscordEmbed, DiscordWebhook

from app.core.config import settings
from app.schemas.vaccine_availability import (
    VaccineAvailabilityExpandedCreateRequest,
)


def discordCallReport(
    va_expanded: VaccineAvailabilityExpandedCreateRequest,
) -> int:

    reasoningString = ""
    bookingMethodsString = ""
    doseString = ""
    vaccineTypeString = ""
    specialNotesString = ""
    tags = ""

    if va_expanded.tagsA == None:
        va_expanded.tagsA = ""

    tags = str(va_expanded.tagsA)

    if tags.find("Cancellation") > 0:
        reasoningString += "Cancellation"

    if tags.find("Expiring") > 0:
        if reasoningString == "":
            reasoningString += "Expiring Doses"
        else:
            reasoningString += " and Expiring Doses"

    if reasoningString == "":
        reasoningString = "General Availability"

    if tags.find("Call Ahead") > 0:
        bookingMethodsString += "Call Ahead"

    if tags.find("Visit Website") > 0:
        if bookingMethodsString == "":
            bookingMethodsString += "Visit Website"
        else:
            bookingMethodsString += ", Visit Website"

    if tags.find("Walk") > 0:
        if bookingMethodsString == "":
            bookingMethodsString += "Walk In"
        else:
            bookingMethodsString += ", Walk In"

    if tags.find("Email") > 0:
        if bookingMethodsString == "":
            bookingMethodsString += "Email"
        else:
            bookingMethodsString += ", Email"

    isFirstDose = 0
    isSecondDose = 0

    if tags.find("1st") > 0:
        isFirstDose = 1

    if tags.find("2nd") > 0:
        isSecondDose = 1

    if isFirstDose & isSecondDose:
        doseString = "First and Second"
    elif isFirstDose:
        doseString = "First Dose Only"
    elif isSecondDose:
        doseString = "Second Dose Only"

    if tags.find("Pfizer") > 0:
        vaccineTypeString = "Pfizer"

    if tags.find("Moderna") > 0:
        vaccineTypeString = "Moderna"

    if tags.find("AstraZeneca") > 0:
        vaccineTypeString = "AstraZeneca"

    if tags.find("Unknown") > 0:
        vaccineTypeString = "Unknown"

    webhook = DiscordWebhook(
        url=settings.DISCORD_WEBHOOK_ADD,
        username="Pharmacy Updates",
        content="<@&835240707241148428>",
    )

    # create embed object for webhook
    # title: `New Availability for ${name} at ${address}, ${city}, ${province}, ${postalCode}`,
    embed = DiscordEmbed(
        title="New Availability for {0} at {1}, {2}, {3}, {4}".format(
            va_expanded.name,
            va_expanded.line1,
            va_expanded.city,
            va_expanded.province,
            va_expanded.postcode,
        ),
        description="New availability was reported through our reporting form. @pharmacy",
    )

    # set author
    embed.set_author(
        name="Pharmacy Updates",
        icon_url="https://vaccinehunters.ca/favicon.ico",
    )

    # add fields to embed
    if va_expanded.phone == None:
        embed.add_embed_field(
            name="Phone Number", value="Not Reported", inline=True
        )
    else:
        embed.add_embed_field(
            name="Phone Number", value=va_expanded.phone, inline=True
        )

    embed.add_embed_field(name="Website", value=va_expanded.url, inline=True)

    if va_expanded.numberAvailable > 0:
        embed.add_embed_field(
            name="Number Available",
            value=va_expanded.numberAvailable,
            inline=True,
        )
    else:
        embed.add_embed_field(
            name="Number Available",
            value="Not Reported",
            inline=True,
        )

    if reasoningString == "":
        embed.add_embed_field(
            name="Reasoning", value="Not Reported", inline=True
        )
    else:
        embed.add_embed_field(
            name="Reasoning", value=reasoningString, inline=True
        )

    if vaccineTypeString == "":
        embed.add_embed_field(
            name="Vaccine Type", value="Not Reported", inline=True
        )
    else:
        embed.add_embed_field(
            name="Vaccine Type", value=vaccineTypeString, inline=True
        )

    if bookingMethodsString == "":
        embed.add_embed_field(
            name="Booking Method", value="Not Reported", inline=True
        )
    else:
        embed.add_embed_field(
            name="Booking Method", value=bookingMethodsString, inline=True
        )

    if doseString == "":
        embed.add_embed_field(name="Doses", value="Not Reported", inline=True)
    else:
        embed.add_embed_field(name="Doses", value=doseString, inline=True)

    if specialNotesString == "":
        embed.add_embed_field(
            name="Special Notes", value="Not Reported", inline=True
        )
    else:
        embed.add_embed_field(
            name="Special Notes", value=doseString, inline=True
        )

    webhook.add_embed(embed)

    response = webhook.execute()

    return 1


def discordCallNoDoses(
    va_expanded: VaccineAvailabilityExpandedCreateRequest,
) -> int:
    webhook = DiscordWebhook(
        url=settings.DISCORD_WEBHOOK_REM,
        username="Pharmacy Updates",
        content="<@&835240707241148428>",
    )

    # create embed object for webhook
    # title: `New Availability for ${name} at ${address}, ${city}, ${province}, ${postalCode}`,
    embed = DiscordEmbed(
        title="No doses left for {0} at {1}, {2}, {3}, {4}".format(
            va_expanded.name,
            va_expanded.line1,
            va_expanded.city,
            va_expanded.province,
            va_expanded.postcode,
        ),
        description="This pharmacy has reported that they no longer have any doses",
    )

    # set author
    embed.set_author(
        name="Pharmacy Updates",
        icon_url="https://vaccinehunters.ca/favicon.ico",
    )

    webhook.add_embed(embed)

    response = webhook.execute()

    return 1
