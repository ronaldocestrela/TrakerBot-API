namespace TrakerBot.Core.Entities;

public class Bookmaker : BaseEntity
{
    public required string Name { get; set; }
    public string? LogoUrl { get; set; }
}
