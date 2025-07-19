namespace TrakerBot.Core.Entities;

public class Telegram : BaseEntity
{
    public required string TelegramId { get; set; }
    public required string Username { get; set; }
    public string? UserId { get; set; }
    public ApplicationUser? User { get; set; }
}
