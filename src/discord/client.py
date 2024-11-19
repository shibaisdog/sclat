from pypresence import Presence
RPC = Presence(1308354144490360943)
def update(start_time,name):
    RPC.update(
        details=f"{name}",
        start=start_time,
        large_image="sclatlogo",
        large_text="Sclat",
    )