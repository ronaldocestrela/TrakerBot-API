namespace TrakerBot.Core.Entities;

public class AffiliateCode : BaseEntity
{
    public required string Code { get; set; }
    public string? UserId { get; set; }
    public ApplicationUser? User { get; set; }
    public string? BookmakerId { get; set; }
    public Bookmaker? Bookmaker { get; set; }
}
