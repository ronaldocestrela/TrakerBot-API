using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TrakerBot.Core.Entities;

namespace TrakerBot.Persistance.Configurations;

public class TelegramConfigurations : IEntityTypeConfiguration<Telegram>
{
    public void Configure(EntityTypeBuilder<Telegram> builder)
    {
        builder.Property(t => t.TelegramId).IsRequired();
        builder.HasIndex(t => t.TelegramId).IsUnique();

        builder.Property(t => t.Username).IsRequired();
        builder.HasIndex(t => t.Username).IsUnique();
        
        builder.HasOne(t => t.User)
            .WithMany(u => u.Telegrams)
            .HasForeignKey(t => t.UserId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
