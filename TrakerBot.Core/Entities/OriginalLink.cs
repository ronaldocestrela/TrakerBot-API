namespace TrakerBot.Core.Entities;

public class OriginalLink : BaseEntity
{
    public required string Url { get; set; }
    public required string ShortenedUrl { get; set; }
    public string? UserId { get; set; }
    public ApplicationUser? User { get; set; }
}
